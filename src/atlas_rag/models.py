from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


Role = Literal["employee", "finance", "hr", "executive"]


@dataclass(slots=True)
class Chunk:
    chunk_id: str
    document_id: str
    title: str
    content: str
    topic: str
    allowed_roles: list[Role]
    source_path: str
    tokens: set[str] = field(default_factory=set)


@dataclass(slots=True)
class RetrievalHit:
    chunk: Chunk
    score: float


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_at: int
    role: Role
    display_name: str


class ChatRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1500)


class SourceItem(BaseModel):
    document_id: str
    title: str
    topic: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    role: Role
    sources: list[SourceItem]
    blocked: bool = False
    reason: str | None = None
    trace_id: str


class HealthResponse(BaseModel):
    status: str
    indexed_documents: int
    indexed_chunks: int
    generated_at: datetime


class UserRecord(BaseModel):
    username: str
    password_hash: str
    display_name: str
    role: Role

