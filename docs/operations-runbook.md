# Operations Runbook

## Health Checks (LiveKit)

```bash
cd lena
lk agent status
lk agent logs --log-type=deploy
```

## SIP Checks (LiveKit)

```bash
lk sip inbound-trunk list
lk sip outbound-trunk list
lk sip dispatch-rule list
```

## Telnyx Checks

```bash
curl -sS -L "https://api.telnyx.com/v2/phone_numbers/<id>" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TELNYX_API_KEY"
```

## Rotation von Keys

- Telnyx: neuen `TELNYX_API_KEY` in LiveKit Agent Secrets setzen
- xAI: neuen `XAI_API_KEY` in LiveKit Agent Secrets setzen
- danach: `lk agent restart`

## Rollback

```bash
cd lena
lk agent versions
lk agent rollback
```

