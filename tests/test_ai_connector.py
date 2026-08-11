from app.connectors.ai import AIConnector

def test_high_value_automation_lead_scores_high():
    result = AIConnector().execute("qualify", {
        "message": "urgent api integration automation webhook",
        "company": "Acme",
        "budget": 6000,
    })
    assert result.ok
    assert result.data["ai_score"] >= 75
    assert result.data["ai_priority"] == "high"
