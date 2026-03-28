from __future__ import annotations

import json
from pathlib import Path

from .models import FeedbackRecord, MemorySnapshot
from .serializer import memory_from_dict, memory_to_dict


class JsonMemoryRepository:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> MemorySnapshot:
        if not self.path.exists():
            return MemorySnapshot()
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return memory_from_dict(payload)

    def save(self, snapshot: MemorySnapshot) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps(memory_to_dict(snapshot), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def append_feedback(self, record: FeedbackRecord) -> MemorySnapshot:
        snapshot = self.load()
        snapshot.feedback.append(record)
        self.save(snapshot)
        return snapshot

