from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .prompts import SUMMARY_SYSTEM_PROMPT
from .state import StrategyAgentState


def build_summary_payload(state: StrategyAgentState) -> dict[str, Any]:
    return {
        "system_prompt": SUMMARY_SYSTEM_PROMPT,
        "market_status": state.market_status,
        "target_exposure": state.target_exposure,
        "market_reason": state.market_reason,
        "buy_candidates": state.buy_candidates[:5],
        "sell_signals": state.sell_signals[:5],
        "trim_signals": state.trim_signals[:5],
        "needs_review_symbols": state.needs_review_symbols,
        "memory_hints": state.memory_hints,
        "errors": state.errors,
    }


def state_to_dict(state: StrategyAgentState) -> dict[str, Any]:
    return asdict(state)

