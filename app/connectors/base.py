from dataclasses import dataclass
from typing import Any

@dataclass
class ConnectorResult:
    ok: bool
    data: dict[str, Any]
    detail: str = ""

class Connector:
    name = "base"

    def execute(self, action: str, payload: dict) -> ConnectorResult:
        raise NotImplementedError
