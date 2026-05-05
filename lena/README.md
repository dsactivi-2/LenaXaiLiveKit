# LiveKit Telesales Agent (DE) – Jobportal-Inserate

LiveKit Agent (Python) mit xAI Grok Voice Agent API (`livekit.plugins.xai`) für deutschsprachige Telesales-Calls zu Jobanzeigen (StepStone/Indeed).

## Setup

```bash
cd livekit-telesales-agent
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

## Deploy (LiveKit Cloud)

Aus dem Projektverzeichnis:

```bash
lk agent create
```

## Konfiguration

- LiveKit: `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET`, optional `LIVEKIT_ROOM`, `LIVEKIT_IDENTITY`
- xAI: `XAI_API_KEY`
- Prompt: `COMPANY_NAME`, `OFFER_NAME`, `TARGET_CUSTOMERS`
