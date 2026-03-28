from __future__ import annotations

from .schemas.input import StrategyAgentRequest
from .schemas.output import MarketSummary, StrategyAgentResponse
from .state import StrategyAgentState
from .tools.market_tools import MarketTools
from .tools.memory_tools import MemoryTools
from .tools.strategy_tools import StrategyTools


class StrategyAgent:
    def __init__(
        self,
        market_tools: MarketTools | None = None,
        strategy_tools: StrategyTools | None = None,
        memory_tools: MemoryTools | None = None,
    ):
        self.market_tools = market_tools or MarketTools()
        self.strategy_tools = strategy_tools or StrategyTools()
        self.memory_tools = memory_tools or MemoryTools("data/memory/strategy_agent_memory.json")

    def run(self, request: StrategyAgentRequest) -> StrategyAgentResponse:
        state = StrategyAgentState(
            request_id=request.request_id,
            trade_date=request.trade_date,
            template_key=request.template_key,
            mode=request.mode,
        )

        memory = self.memory_tools.load_memory()
        if memory.feedback:
            state.memory_hints.append(f"已有人工反馈 {len(memory.feedback)} 条")

        data_status = self.market_tools.check_daily_data_ready(request.trade_date)
        state.data_status = data_status.status
        state.trade_date = data_status.trade_date
        if data_status.status != "ready":
            state.errors.append(data_status.detail)
            return self._build_response(state)

        try:
            plan = self.strategy_tools.generate_strategy_plan(
                trade_date=state.trade_date,
                template_key=state.template_key,
            )
        except Exception as exc:
            state.errors.append(str(exc))
            state.summary = self._build_summary(state)
            return self._build_response(state)
        state.market_status = str(plan.get("market_status") or "unknown")
        state.target_exposure = float(plan.get("target_exposure") or 0.0)
        state.market_reason = str(plan.get("market_reason") or "")

        stocks = list(plan.get("stocks") or [])
        signals = list(plan.get("signals") or [])

        state.buy_candidates = [item for item in stocks if str(item.get("action") or "") == "buy"]
        state.sell_signals = [item for item in signals if str(item.get("signal_type") or "") == "sell"]
        state.trim_signals = [item for item in signals if str(item.get("signal_type") or "") == "trim"]
        state.hold_positions = [item for item in stocks if str(item.get("action") or "") == "hold"]
        state.watchlist = [item for item in stocks if str(item.get("action") or "") == "avoid"][:10]
        state.needs_review_symbols = self._pick_review_symbols(stocks, signals)
        state.summary = self._build_summary(state)
        return self._build_response(state)

    def _pick_review_symbols(self, stocks: list[dict], signals: list[dict]) -> list[str]:
        review_symbols: list[str] = []
        for item in stocks:
            action = str(item.get("action") or "")
            score_total = float(item.get("score_total") or 0.0)
            if action == "buy" and score_total < 75:
                review_symbols.append(str(item.get("symbol") or ""))
            if action in {"sell", "trim"} and score_total > 80:
                review_symbols.append(str(item.get("symbol") or ""))
        for item in signals:
            if str(item.get("signal_type") or "") == "trim":
                review_symbols.append(str(item.get("symbol") or ""))
        return [symbol for symbol in dict.fromkeys(review_symbols) if symbol]

    def _build_summary(self, state: StrategyAgentState) -> str:
        if state.errors:
            return f"数据暂未就绪或策略计划生成失败：{state.errors[0]}"
        return (
            f"交易日 {state.trade_date}，市场状态为 {state.market_status}，"
            f"建议总仓位 {state.target_exposure:.2f}。"
            f"买入候选 {len(state.buy_candidates)} 只，"
            f"卖出信号 {len(state.sell_signals)} 只，"
            f"减仓信号 {len(state.trim_signals)} 只。"
        )

    def _build_response(self, state: StrategyAgentState) -> StrategyAgentResponse:
        market = MarketSummary(
            status=state.market_status,
            reason=state.market_reason,
            target_exposure=state.target_exposure,
        )
        return StrategyAgentResponse(
            request_id=state.request_id,
            trade_date=state.trade_date,
            template_key=state.template_key,
            market=market,
            buy=state.buy_candidates,
            trim=state.trim_signals,
            sell=state.sell_signals,
            hold=state.hold_positions,
            watchlist=state.watchlist,
            needs_review_symbols=state.needs_review_symbols,
            summary=state.summary,
            errors=state.errors,
        )
