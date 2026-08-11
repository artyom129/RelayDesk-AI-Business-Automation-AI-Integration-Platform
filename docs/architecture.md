# Architecture

RelayDesk AI separates orchestration from integrations.

```text
Webhook / Manual / Scheduled Trigger
               |
               v
        Workflow Engine
               |
      +--------+---------+---------+---------+
      |        |         |         |         |
 Transform     AI       CRM      Sheets    Email/Chatbot
      |        |         |         |         |
      +--------+---------+---------+---------+
               |
          Run Telemetry
               |
      SQLite + Audit + DLQ
```

Each connector implements a shared interface. Production adapters can call HubSpot, Pipedrive, Salesforce, Gmail, SendGrid, Google Sheets, Telegram, Slack, OpenAI, Anthropic, or other APIs.

The workflow engine owns sequencing, retry policy, failure tracking, dead-letter storage and output handoff.
