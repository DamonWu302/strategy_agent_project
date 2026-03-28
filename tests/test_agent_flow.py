from strategy_agent.agent import StrategyAgent
from strategy_agent.schemas.input import StrategyAgentRequest
from strategy_agent.tools.market_tools import MarketDataStatus


class FakeMarketTools:
    def check_daily_data_ready(self, trade_date):
        return MarketDataStatus(status="ready", trade_date=trade_date or "2026-03-27", detail="ok")


class FakeStrategyTools:
    def generate_strategy_plan(self, trade_date, template_key):
        return {
            "trade_date": trade_date,
            "market_status": "open",
            "market_reason": "fake market ready",
            "target_exposure": 1.0,
            "stocks": [
                {"symbol": "600000", "action": "buy", "score_total": 72},
                {"symbol": "600001", "action": "hold", "score_total": 81},
            ],
            "signals": [
                {"symbol": "600002", "signal_type": "trim"},
            ],
        }


class FakeMemoryTools:
    def load_memory(self):
        class Snapshot:
            feedback = []

        return Snapshot()


def test_agent_returns_structured_response():
    agent = StrategyAgent(
        market_tools=FakeMarketTools(),
        strategy_tools=FakeStrategyTools(),
        memory_tools=FakeMemoryTools(),
    )
    response = agent.run(StrategyAgentRequest())
    assert response.market.status == "open"
    assert len(response.buy) == 1
    assert "600000" in response.needs_review_symbols
