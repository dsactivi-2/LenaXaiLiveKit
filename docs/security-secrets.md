# Security / Secrets

## Grundregeln

- Keine Keys in Git committen.
- Nutze LiveKit Cloud Agent Secrets für Production.
- Lokale Secrets nur in `.env` / `secrets.env` (gitignored).

## Dateien (gitignored)

- `lena/secrets.env`
- `lena/telnyx_*.json`

## Empfohlenes Vorgehen

1) Lokal `.env` nutzen (dev)
2) Für Deploy: `secrets.env` erzeugen, dann `lk agent create/deploy --secrets-file secrets.env`
3) Rotation: `lk agent update-secrets`

