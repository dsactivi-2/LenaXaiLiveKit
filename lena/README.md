# LiveKit Telesales Agent (DE) – Jobportal-Inserate

LiveKit Agent (Python) mit xAI Grok Voice Agent API (`livekit.plugins.xai`) für deutschsprachige Telesales-Calls zu Jobanzeigen (StepStone/Indeed).

> Projekt-Überblick & Doku: `../README.md` und `../docs/README.md`

## Setup

```bash
cd livekit-telesales-agent/lena
cp .env.example .env
```

Install (uv):

```bash
uv sync
```

oder pip:

```bash
pip install -e .
```

## Run

```bash
uv run agent.py dev
```

## Konfiguration (wichtig)

- xAI Realtime: `XAI_API_KEY`
- Turn detection (telephony): `LENA_TURN_*` (Defaults in `realtime_settings.py`)
- Branding/Offer: `LENA_COMPANY_NAME`, `LENA_OFFER_NAME`, `LENA_TARGET_CUSTOMERS`

## Deploy (LiveKit Cloud)

Aus dem Projektverzeichnis:

```bash
lk cloud auth
cp secrets.env.example secrets.env
# secrets.env befüllen (keine Secrets committen)
lk agent create --region eu-central --secrets-file secrets.env .
```

## Voraussetzungen

- LiveKit (für CLI/Cloud): `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`
- Telnyx (für Setup/Automation): `TELNYX_API_KEY`

Telephony Setup (Telnyx ↔ LiveKit): `../docs/telnyx-livekit-setup.md`
