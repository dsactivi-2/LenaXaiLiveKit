# Troubleshooting

## `lk agent create`: Secret ist leer

Fehler: `secret XAI_API_KEY is empty`

- Prüfe ob dein `secrets.env` den Wert wirklich enthält (kein `${VAR}` ohne gesetzte Env)

## Telnyx Auth / 401

- Prüfe `TELNYX_API_KEY`
- Test: `GET /v2/phone_numbers/<id>`

## Outbound Calls scheitern / falsche Auth

- Stelle sicher, dass LiveKit Outbound Trunk den Header `X-Telnyx-Username=<user>` mitsendet:
  - `lk sip outbound-trunk list` → “Headers” Spalte

