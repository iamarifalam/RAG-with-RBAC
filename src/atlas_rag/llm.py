from __future__ import annotations

import json
import urllib.request

from atlas_rag.config import get_settings
from atlas_rag.guardrails import redact_pii
from atlas_rag.models import RetrievalHit, Role


class LLMClient:
    def answer(self, question: str, hits: list[RetrievalHit], role: Role) -> str:
        settings = get_settings()
        if settings.llm_mode == "openai_compatible":
            return self._call_openai_compatible(question, hits, role)
        return self._mock_answer(question, hits, role)

    def _mock_answer(self, question: str, hits: list[RetrievalHit], role: Role) -> str:
        preamble = f"Role `{role}` is authorized to view the following grounded answer."
        evidence = " ".join(redact_pii(hit.chunk.content) for hit in hits[: get_settings().max_context_chunks])
        return f"{preamble}\n\nAnswer to: {question}\n\n{evidence}"

    def _call_openai_compatible(self, question: str, hits: list[RetrievalHit], role: Role) -> str:
        settings = get_settings()
        if not settings.openai_compatible_base_url or not settings.openai_compatible_api_key:
            return self._mock_answer(question, hits, role)

        context = "\n\n".join(
            f"[{hit.chunk.title} | {hit.chunk.topic}] {redact_pii(hit.chunk.content)}" for hit in hits
        )
        payload = {
            "model": settings.openai_compatible_model or "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are an internal enterprise assistant. Answer only from provided context. "
                        "If context is insufficient, say so clearly."
                    ),
                },
                {"role": "user", "content": f"Role: {role}\nQuestion: {question}\n\nContext:\n{context}"},
            ],
            "temperature": 0.2,
        }
        request = urllib.request.Request(
            url=f"{settings.openai_compatible_base_url.rstrip('/')}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bearer {settings.openai_compatible_api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]

