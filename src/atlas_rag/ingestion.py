from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

from atlas_rag.models import Chunk
from atlas_rag.retrieval import parse_document, split_into_chunks


class DocumentStore:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.data_dir = root / "data" / "documents"
        self.storage_dir = root / "storage"
        self.index_path = self.storage_dir / "index.json"

    def build_index(self) -> list[Chunk]:
        chunks: list[Chunk] = []
        for path in sorted(self.data_dir.glob("*.md")):
            title, topic, allowed_roles, body = parse_document(path)
            document_id = path.stem
            chunks.extend(
                split_into_chunks(
                    document_id=document_id,
                    title=title,
                    topic=topic,
                    allowed_roles=allowed_roles,
                    body=body,
                    source_path=str(path),
                )
            )
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(
            json.dumps(
                [
                    {
                        **asdict(chunk),
                        "tokens": sorted(chunk.tokens),
                    }
                    for chunk in chunks
                ],
                indent=2,
            ),
            encoding="utf-8",
        )
        return chunks

    def load_index(self) -> list[Chunk]:
        if not self.index_path.exists():
            return self.build_index()
        records = json.loads(self.index_path.read_text(encoding="utf-8"))
        return [
            Chunk(
                chunk_id=record["chunk_id"],
                document_id=record["document_id"],
                title=record["title"],
                content=record["content"],
                topic=record["topic"],
                allowed_roles=record["allowed_roles"],
                source_path=record["source_path"],
                tokens=set(record["tokens"]),
            )
            for record in records
        ]

