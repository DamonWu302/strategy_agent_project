from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class StrategyAgentState:
    request_id: str
    trade_date: str | None
    template_key: str
    mode: str
    data_status: str = "unknown"
    market_status: str = "unknown"
    target_exposure: float = 0.0
    summary: str = ""
    market_reason: str = ""
    buy_candidates: list[dict] = field(default_factory=list)
    sell_signals: list[dict] = field(default_factory=list)
    trim_signals: list[dict] = field(default_factory=list)
    hold_positions: list[dict] = field(default_factory=list)
    watchlist: list[dict] = field(default_factory=list)
    needs_review_symbols: list[str] = field(default_factory=list)
    memory_hints: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

