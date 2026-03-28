from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class MarketDataStatus:
    status: str
    trade_date: str | None
    detail: str


class MarketTools:
    def get_latest_trade_date(self) -> str:
        return datetime.now().strftime("%Y-%m-%d")

    def check_daily_data_ready(self, trade_date: str | None) -> MarketDataStatus:
        return MarketDataStatus(
            status="ready",
            trade_date=trade_date or self.get_latest_trade_date(),
            detail="骨架版本未接入 stock_analysis，默认返回 ready。",
        )

