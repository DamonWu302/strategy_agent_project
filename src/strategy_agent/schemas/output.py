from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class MarketSummary:
    status: str
    reason: str
    target_exposure: float


@dataclass(slots=True)
class StrategyAgentResponse:
    request_id: str
    trade_date: str | None
    template_key: str
    market: MarketSummary
    buy: list[dict] = field(default_factory=list)
    trim: list[dict] = field(default_factory=list)
    sell: list[dict] = field(default_factory=list)
    hold: list[dict] = field(default_factory=list)
    watchlist: list[dict] = field(default_factory=list)
    needs_review_symbols: list[str] = field(default_factory=list)
    summary: str = ""
    errors: list[str] = field(default_factory=list)

