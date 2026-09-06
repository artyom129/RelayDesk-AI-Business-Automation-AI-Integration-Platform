**English** | [Русский](README_RU.md)

<div align="center">

# RelayDesk AI

### Business Automation & AI Integration Control Center

**Python · FastAPI · CRM · Webhooks · AI Qualification · Google Sheets · Email · Chatbots · Docker**

</div>

RelayDesk AI is a production-style business automation platform for connecting lead forms, CRMs, spreadsheets, email systems, chatbots, and AI services through reliable workflows.

It is designed around a common client problem: data enters through one tool, must be cleaned and qualified, then needs to reach several other systems without manual copy/paste or silent failures.

## Demo workflow

```text
Website / Form / Webhook
          ↓
   Normalize payload
          ↓
    AI qualification
          ↓
      CRM upsert
          ↓
 Google Sheets logging
          ↓
 Customer email
          ↓
 Admin chatbot alert
```

Every workflow execution has step-level telemetry, retries, persistent audit history, and dead-letter handling.

## Highlights

- FastAPI REST backend
- Webhook-driven automation
- Reusable workflow engine
- Pluggable connector architecture
- CRM-style contact synchronization
- Google Sheets-style logging connector
- Email workflow connector
- Chatbot/admin notification connector
- AI lead qualification and priority scoring
- Payload normalization
- Step-level execution telemetry
- Automatic retries
- Dead-letter queue for failed steps
- Persistent SQLite audit history
- Operations dashboard
- Swagger/OpenAPI docs
- Docker / docker-compose
- GitHub Actions
- Automated tests
- Demo data and one-click demo run
- No paid API keys required for portfolio demo mode

## Why it maps to real automation work

The included connectors are deterministic demo adapters, but the connector interface is intentionally production-oriented. A live project can swap them for:

- HubSpot / Pipedrive / Salesforce
- Gmail / Outlook / SendGrid
- Google Sheets / Airtable
- Telegram / Slack / WhatsApp
- OpenAI / Anthropic
- n8n / Make webhook endpoints
- WordPress / WooCommerce
- Custom REST APIs

without changing the orchestration layer.

## Quick start

```bash
python -m venv .venv
```

Windows:

```bat
.venv\Scripts\activate
pip install -r requirements.txt
python seed_demo.py
uvicorn app.main:app --reload
```

macOS / Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
python seed_demo.py
uvicorn app.main:app --reload
```

Open:

- Dashboard: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

## Test a webhook

```bash
curl -X POST http://127.0.0.1:8000/webhooks/lead \
  -H "Content-Type: application/json" \
  -d @examples/lead-webhook.json
```

## API surface

- `POST /webhooks/lead` — execute AI lead automation
- `POST /workflows/{id}/run` — manual workflow execution
- `GET /api/workflows` — workflow definitions
- `GET /api/runs` — execution history
- `GET /api/runs/{id}` — step-level run details
- `GET /api/contacts` — CRM-style synchronized contacts
- `GET /health` — service health

## Portfolio positioning

RelayDesk AI is a personal demonstration project built to showcase Python/FastAPI backend development, API integration, workflow automation, AI-assisted business logic, CRM/data synchronization, retries, observability, and maintainable connector design.

It does not claim to be client work.
