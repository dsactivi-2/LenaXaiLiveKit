# LenaXaiLiveKit

Deutschsprachiger Voice‑Telesales‑Agent auf **LiveKit Agents** mit **xAI Realtime Voice** und optionaler **Telnyx SIP‑Telephony** Integration (Inbound/Outbound).

## Repository-Struktur

- `lena/` – produktiver Agent „Lena“ (DE), inkl. Deploy zu LiveKit Cloud
- `mxagent/` – Referenz/Starter-Projekt (Template) und Experimente
- `docs/` – Setup-Guides, Runbooks, Troubleshooting

## Quickstart (lokal)

```bash
cd lena
cp ../.env.example .env
# .env ausfüllen (siehe docs)
uv sync
uv run agent.py dev
```

## Deploy (LiveKit Cloud)

```bash
cd lena
lk cloud auth
lk agent create --region eu-central --secrets-file secrets.env .
```

## Self-host (Docker)

Dieses Repo enthält eine minimale `docker-compose.yml` im Repo-Root, um den Agent-Worker außerhalb von LiveKit Cloud laufen zu lassen.

- Image: `denis8686/lenaxailivekit-lena:<version>` (empfohlen) oder `:latest`
- Feature Flags:
  - `ENABLE_TOOL_CALLING` (default: `true`)
  - `ENABLE_WEB_SEARCH` / `ENABLE_X_SEARCH` (default: `false`; erfordert zusätzliche Provider-Integration)
  - `PROMETHEUS_ENABLED` (default: `true`), Port via `PROMETHEUS_PORT` (default: `8000`)

## Telephony (Telnyx SIP) – Überblick

Für Telnyx brauchst du:

- eine Telnyx Nummer (E.164, z.B. `+49...`)
- eine Telnyx FQDN Connection auf deinen LiveKit SIP Endpoint
- LiveKit SIP Trunks (Inbound + Outbound) + Dispatch Rule

Anleitung: `docs/telnyx-livekit-setup.md`.

## Sicherheit

Keine Secrets committen:

- `secrets.env` bleibt lokal und wird von `.gitignore` ausgeschlossen
- LiveKit Cloud Secrets werden via `lk agent create/update-secrets` gesetzt

Details: `docs/security-secrets.md`.
