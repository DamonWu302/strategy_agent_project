from __future__ import annotations

from pathlib import Path

from ..memory.models import FeedbackRecord, MemorySnapshot
from ..memory.repository import JsonMemoryRepository


class MemoryTools:
    def __init__(self, memory_path: str | Path):
        self.repo = JsonMemoryRepository(memory_path)

    def load_memory(self) -> MemorySnapshot:
        return self.repo.load()

    def record_feedback(self, trade_date: str, symbol: str, action: str, decision: str, note: str = "") -> MemorySnapshot:
        record = FeedbackRecord(
            trade_date=trade_date,
            symbol=symbol,
            action=action,
            decision=decision,
            note=note,
        )
        return self.repo.append_feedback(record)

