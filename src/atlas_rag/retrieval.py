from __future__ import annotations

import math
import re
from collections import Counter
from pathlib import Path

from atlas_rag.models import Chunk, RetrievalHit

TOKEN_PATTERN = re.compile(r"[a-zA-Z0-9]{2,}")


def tokenize(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_PATTERN.findall(text)]


def split_into_chunks(document_id: str, title: str, topic: str, allowed_roles: list[str], body: str, source_path: str) -> list[Chunk]:
    paragraphs = [part.strip() for part in body.split("\n\n") if part.strip()]
    chunks: list[Chunk] = []
    for idx, paragraph in enumerate(paragraphs, start=1):
        chunks.append(
            Chunk(
                chunk_id=f"{document_id}-{idx}",
                document_id=document_id,
                title=title,
                content=paragraph,
                topic=topic,
                allowed_roles=allowed_roles,  # type: ignore[arg-type]
                source_path=source_path,
                tokens=set(tokenize(paragraph)),
            )
        )
    return chunks


class Retriever:
    def __init__(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.doc_count = len(chunks)
        self.term_document_frequency = Counter()
        for chunk in chunks:
            self.term_document_frequency.update(chunk.tokens)

    def search(self, query: str, top_k: int = 4) -> list[RetrievalHit]:
        query_tokens = tokenize(query)
        if not query_tokens:
            return []
        query_counter = Counter(query_tokens)
        scored: list[RetrievalHit] = []
        for chunk in self.chunks:
            overlap = set(query_tokens) & chunk.tokens
            if not overlap:
                continue
            score = 0.0
            for token in overlap:
                tf = query_counter[token]
                idf = math.log((1 + self.doc_count) / (1 + self.term_document_frequency[token])) + 1
                score += tf * idf
            score = score / max(len(chunk.tokens), 20)
            scored.append(RetrievalHit(chunk=chunk, score=score))
        scored.sort(key=lambda hit: hit.score, reverse=True)
        return scored[:top_k]


def parse_document(path: Path) -> tuple[str, str, list[str], str]:
    text = path.read_text(encoding="utf-8")
    header, _, body = text.partition("\n\n")
    metadata: dict[str, str] = {}
    for line in header.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", maxsplit=1)
        metadata[key.strip().lower()] = value.strip()
    title = metadata.get("title", path.stem)
    topic = metadata.get("topic", "policy")
    allowed_roles = [item.strip() for item in metadata.get("roles", "employee").split(",")]
    return title, topic, allowed_roles, body.strip()

