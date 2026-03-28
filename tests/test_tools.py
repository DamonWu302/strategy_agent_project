from strategy_agent.tools.market_tools import MarketTools


def test_market_tools_returns_trade_date():
    tools = MarketTools()
    status = tools.check_daily_data_ready(None)
    assert status.status == "ready"
    assert status.trade_date
