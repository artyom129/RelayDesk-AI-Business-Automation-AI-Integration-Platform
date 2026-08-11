from .base import Connector, ConnectorResult

class TransformConnector(Connector):
    name = "transform"

    def execute(self, action: str, payload: dict) -> ConnectorResult:
        data = dict(payload)
        if "email" in data:
            data["email"] = str(data["email"]).strip().lower()
        if "name" in data:
            data["name"] = " ".join(str(data["name"]).split())
        if action == "normalize_lead":
            data["normalized"] = True
        return ConnectorResult(True, data, "Payload normalized")
