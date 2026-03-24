from __future__ import annotations

from contextlib import asynccontextmanager
import secrets
from datetime import datetime, timezone
from pathlib import Path

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import jinja2

from atlas_rag.auth import decode_token, issue_token, seed_users, verify_password
from atlas_rag.config import get_settings
from atlas_rag.guardrails import detect_blocked_question, filter_hits_for_role
from atlas_rag.ingestion import DocumentStore
from atlas_rag.llm import LLMClient
from atlas_rag.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    LoginRequest,
    SourceItem,
    TokenResponse,
    UserRecord,
)
from atlas_rag.monitoring import RequestTimer, logger, metrics
from atlas_rag.retrieval import Retriever

ROOT = Path(__file__).resolve().parents[2]
jinja_env = jinja2.Environment(
    loader=jinja2.FileSystemLoader(str(ROOT / "templates")),
    cache_size=0,  # Disable caching
)
templates = Jinja2Templates(env=jinja_env)
auth_scheme = HTTPBearer()

document_store = DocumentStore(ROOT)
users = seed_users()
llm_client = LLMClient()
retriever = Retriever(document_store.load_index())


@asynccontextmanager
async def lifespan(_: FastAPI):
    metrics.increment("startup")
    logger.info("Indexed %s chunks for Atlas RAG Assistant", len(retriever.chunks))
    yield


app = FastAPI(title=get_settings().app_name, lifespan=lifespan)
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)) -> UserRecord:
    payload = decode_token(credentials.credentials)
    user = users.get(payload["sub"])
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unknown user")
    return user


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    demo_users_list = []
    for user in users.values():
        demo_users_list.append({
            "username": user.username,
            "password": demo_password_for(user.username),
            "role": user.role
        })
    
    # Use jinja_env to render the template directly
    template = jinja_env.get_template("index.html")
    html = template.render(
        app_name=get_settings().app_name,
        demo_users=demo_users_list,
    )
    return HTMLResponse(content=html)


def demo_password_for(username: str) -> str:
    passwords = {
        "alice.finance": "FinanceDemo123",
        "harry.hr": "HrDemo123",
        "erin.exec": "ExecDemo123",
        "emma.employee": "EmployeeDemo123",
    }
    return passwords[username]


@app.post("/api/auth/login", response_model=TokenResponse)
def login(payload: LoginRequest) -> TokenResponse:
    with RequestTimer():
        metrics.increment("login_attempt")
        username = payload.username
        password = payload.password
        user = users.get(username)
        if user is None or not verify_password(password, user.password_hash):
            metrics.increment("login_failure")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token, expires_at = issue_token(user.username, user.role)
        metrics.increment("login_success")
        return TokenResponse(
            access_token=token,
            expires_at=expires_at,
            role=user.role,
            display_name=user.display_name,
        )


@app.post("/api/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, user: UserRecord = Depends(get_current_user)) -> ChatResponse:
    with RequestTimer():
        metrics.increment("chat_request")
        blocked_reason = detect_blocked_question(payload.question, user.role)
        if blocked_reason:
            metrics.increment("guardrail_block")
            return ChatResponse(
                answer="I can't answer that request.",
                role=user.role,
                sources=[],
                blocked=True,
                reason=blocked_reason,
                trace_id=secrets.token_hex(8),
            )

        hits = retriever.search(payload.question, top_k=get_settings().max_context_chunks)
        hits = filter_hits_for_role(hits, user.role)
        if not hits or hits[0].score < get_settings().min_retrieval_score:
            metrics.increment("retrieval_miss")
            return ChatResponse(
                answer="I couldn't find grounded evidence for that request in the indexed company documents.",
                role=user.role,
                sources=[],
                blocked=False,
                reason="insufficient_context",
                trace_id=secrets.token_hex(8),
            )

        answer = llm_client.answer(payload.question, hits, user.role)
        metrics.increment("chat_success")
        return ChatResponse(
            answer=answer,
            role=user.role,
            sources=[
                SourceItem(
                    document_id=hit.chunk.document_id,
                    title=hit.chunk.title,
                    topic=hit.chunk.topic,
                    score=round(hit.score, 4),
                )
                for hit in hits
            ],
            trace_id=secrets.token_hex(8),
        )


@app.post("/api/admin/reindex")
def reindex(user: UserRecord = Depends(get_current_user)) -> dict[str, int | str]:
    if user.role != "executive":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Executive role required")
    chunks = document_store.build_index()
    global retriever
    retriever = Retriever(chunks)
    metrics.increment("reindex")
    return {"status": "ok", "chunks": len(chunks)}


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        indexed_documents=len({chunk.document_id for chunk in retriever.chunks}),
        indexed_chunks=len(retriever.chunks),
        generated_at=datetime.now(timezone.utc),
    )


@app.get("/metrics", response_class=PlainTextResponse)
def metric_endpoint() -> str:
    return metrics.render_prometheus()
