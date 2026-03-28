from __future__ import annotations

from pathlib import Path
import sys


def _ensure_stock_analysis_importable() -> None:
    root = Path(__file__).resolve().parents[4] / "stock_analysis" / "stock_analysis"
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


class BacktestTools:
    def run_backtest(self, config: dict | None = None) -> dict:
        _ensure_stock_analysis_importable()
        from stock_analysis.service import StockAnalysisService

        service = StockAnalysisService()
        return service.run_backtest(config=config)

