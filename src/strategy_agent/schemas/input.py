from __future__ import annotations

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class StrategyAgentRequest:
    template_key: str = "return_priority"
    trade_date: str | None = None
    mode: str = "daily_brief"
    include_watchlist: bool = True
    include_positions: bool = True
    request_id: str = field(default_factory=lambda: str(uuid4()))

