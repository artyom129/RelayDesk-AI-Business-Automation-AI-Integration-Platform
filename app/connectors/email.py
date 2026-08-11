from .base import Connector, ConnectorResult

class EmailConnector(Connector):
    name = "email"

    def execute(self, action: str, payload: dict) -> ConnectorResult:
        target = payload.get("email")
        if not target:
            return ConnectorResult(False, payload, "Email connector missing recipient")
        data = dict(payload)
        data["email_status"] = "queued"
        data["email_template"] = action
        return ConnectorResult(True, data, f"Email '{action}' queued for {target}")
