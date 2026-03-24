from __future__ import annotations

import re

from atlas_rag.config import get_settings
from atlas_rag.models import RetrievalHit, Role

PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    re.compile(r"\b(?:\d[ -]*?){13,16}\b"),
    re.compile(r"\b[\w\.-]+@[\w\.-]+\.\w+\b"),
]

TOPIC_KEYWORDS = {
    "finance": {"budget", "expense", "invoice", "revenue", "payroll", "forecast", "finance"},
    "hr": {"employee", "hiring", "leave", "performance", "hr", "benefits", "payroll"},
    "marketing": {"campaign", "marketing", "lead", "brand", "channel"},
    "operations": {"ops", "on-call", "incident", "sla", "inventory", "operations"},
    "policy": {"policy", "compliance", "security", "approval"},
    "security": {"security", "access", "rbac", "credential", "audit"},
}

ROLE_TOPICS: dict[Role, set[str]] = {
    "employee": {"policy", "operations", "marketing"},
    "finance": {"finance", "policy", "operations"},
    "hr": {"hr", "policy", "operations"},
    "executive": set(TOPIC_KEYWORDS),
}


def redact_pii(text: str) -> str:
    redacted = text
    for pattern in PII_PATTERNS:
        redacted = pattern.sub("[REDACTED]", redacted)
    return redacted


def detect_blocked_question(question: str, role: Role) -> str | None:
    lowered = question.lower()
    normalized_tokens = set(re.findall(r"[a-z0-9]+", lowered))
    matched_topics = {
        topic for topic, keywords in TOPIC_KEYWORDS.items() if keywords & normalized_tokens
    }
    allowed_topics = ROLE_TOPICS[role]
    if matched_topics and matched_topics.isdisjoint(allowed_topics):
        return "Question appears to target data outside the caller's allowed domain."
    if not matched_topics and not any(token in normalized_tokens for token in get_settings().allowed_topics):
        return "Question is out of scope for the enterprise assistant."
    return None


def filter_hits_for_role(hits: list[RetrievalHit], role: Role) -> list[RetrievalHit]:
    return [hit for hit in hits if role in hit.chunk.allowed_roles]
