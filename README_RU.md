# RelayDesk AI

[English](README.md) | **Русский**

### Центр бизнес-автоматизации и AI-интеграций

**Python · FastAPI · CRM · Webhooks · AI Qualification · Google Sheets · Email · Chatbots · Docker**

RelayDesk AI — production-style платформа для связывания форм заявок, CRM, таблиц, email, чат-ботов и AI-сервисов через надёжные workflow.

## Проблема

Во многих компаниях данные приходят из одного сервиса, затем их нужно очистить, оценить и отправить сразу в несколько других систем. При ручной обработке возникают дубли, задержки и незаметные ошибки интеграций.

## Demo workflow

```text
Сайт / форма / webhook
          ↓
 Нормализация payload
          ↓
   AI qualification
          ↓
      CRM upsert
          ↓
 Google Sheets logging
          ↓
   Email клиенту
          ↓
  Alert администратору
```

Каждый запуск сохраняет telemetry по шагам, retries, audit history и dead-letter состояние.

## Возможности

- FastAPI REST backend;
- webhook-driven automation;
- reusable workflow engine;
- pluggable connector architecture;
- CRM-style синхронизация контактов;
- Google Sheets-style logging;
- email workflow connector;
- chatbot/admin notifications;
- AI qualification и priority scoring;
- нормализация payload;
- telemetry по каждому шагу;
- automatic retries;
- dead-letter queue;
- SQLite audit history;
- operations dashboard;
- Swagger/OpenAPI;
- Docker / docker-compose;
- GitHub Actions и тесты;
- demo-режим без платных API ключей.

## Как можно адаптировать

Архитектура позволяет заменить demo-connectors на реальные интеграции с HubSpot, Pipedrive, Salesforce, Gmail, Outlook, SendGrid, Google Sheets, Airtable, Telegram, Slack, WhatsApp, OpenAI, Anthropic, n8n, Make, WordPress или любыми REST API.

## Запуск

Windows:

```bat
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python seed_demo.py
uvicorn app.main:app --reload
```

macOS / Linux:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python seed_demo.py
uvicorn app.main:app --reload
```

Открыть:

- Dashboard: `http://127.0.0.1:8000`
- Swagger: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/health`

Проект демонстрирует Python/FastAPI backend, API integration, workflow automation, AI-assisted business logic, data synchronization, retries и observability. Это личный демонстрационный проект.
