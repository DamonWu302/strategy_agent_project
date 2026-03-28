from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class FeedbackRecord:
    trade_date: str
    symbol: str
    action: str
    decision: str
    note: str = ""


@dataclass(slots=True)
class MemorySnapshot:
    feedback: list[FeedbackRecord] = field(default_factory=list)
    preferences: dict[str, str] = field(default_factory=dict)

