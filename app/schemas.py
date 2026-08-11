from pydantic import BaseModel, Field

class WebhookPayload(BaseModel):
    name: str = ""
    email: str
    company: str = ""
    message: str = ""
    budget: float = 0
    source: str = "website"

class WorkflowCreate(BaseModel):
    name: str
    trigger_type: str = "webhook"
    steps: list[dict] = Field(default_factory=list)

class ManualRunRequest(BaseModel):
    payload: dict = Field(default_factory=dict)
