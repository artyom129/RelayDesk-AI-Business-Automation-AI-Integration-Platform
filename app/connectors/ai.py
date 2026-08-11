from .base import Connector, ConnectorResult

KEYWORDS = {
    "urgent": 20,
    "automation": 15,
    "api": 15,
    "crm": 12,
    "integration": 12,
    "fastapi": 10,
    "webhook": 10,
}

class AIConnector(Connector):
    name = "ai"

    def execute(self, action: str, payload: dict) -> ConnectorResult:
        text = " ".join([
            str(payload.get("message", "")),
            str(payload.get("company", "")),
            str(payload.get("source", "")),
        ]).lower()
        score = 35
        score += min(int(float(payload.get("budget", 0)) / 250), 30)
        for word, points in KEYWORDS.items():
            if word in text:
                score += points
        score = min(score, 100)
        priority = "high" if score >= 75 else "medium" if score >= 50 else "normal"
        data = dict(payload)
        data["ai_score"] = score
        data["ai_priority"] = priority
        data["ai_summary"] = f"{priority.title()} priority lead scored {score}/100"
        return ConnectorResult(True, data, "AI lead qualification completed")
