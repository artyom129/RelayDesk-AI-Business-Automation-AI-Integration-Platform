from .base import Connector, ConnectorResult

class ChatbotConnector(Connector):
    name = "chatbot"

    def execute(self, action: str, payload: dict) -> ConnectorResult:
        data = dict(payload)
        data["chatbot_action"] = action
        data["notification_status"] = "sent"
        return ConnectorResult(True, data, "Chatbot/admin notification sent")
