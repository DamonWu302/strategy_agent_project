from __future__ import annotations

from dataclasses import asdict
import json

from .agent import StrategyAgent
from .schemas.input import StrategyAgentRequest


def main() -> None:
    agent = StrategyAgent()
    request = StrategyAgentRequest()
    response = agent.run(request)
    print(json.dumps(asdict(response), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
