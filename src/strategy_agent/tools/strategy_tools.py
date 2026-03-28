from __future__ import annotations

from pathlib import Path
import sys


def _ensure_stock_analysis_importable() -> None:
    root = Path(__file__).resolve().parents[4] / "stock_analysis" / "stock_analysis"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


class StrategyTools:
    def generate_strategy_plan(self, trade_date: str | None, template_key: str) -> dict:
        _ensure_stock_analysis_importable()
        from stock_analysis.service import StockAnalysisService

        service = StockAnalysisService()
        return service.generate_strategy_plan(trade_date=trade_date, template_key=template_key)

    def get_strategy_positions(self, trade_date: str | None, template_key: str) -> list[dict]:
        _ensure_stock_analysis_importable()
        from stock_analysis.service import StockAnalysisService

        service = StockAnalysisService()
        return service.strategy_positions(trade_date=trade_date, template_key=template_key)

