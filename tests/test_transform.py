from app.connectors.transform import TransformConnector

def test_transform_normalizes_email_and_name():
    result = TransformConnector().execute("normalize_lead", {
        "email": "  TEST@Example.COM ",
        "name": "  Alex   Morgan  ",
    })
    assert result.ok
    assert result.data["email"] == "test@example.com"
    assert result.data["name"] == "Alex Morgan"
