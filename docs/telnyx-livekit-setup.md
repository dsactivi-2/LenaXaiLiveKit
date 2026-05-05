# Telnyx ↔ LiveKit Telephony Setup (SIP)

Ziel: Inbound/Outbound Calls über Telnyx zu LiveKit routen, so dass dein LiveKit Agent Telephony nutzen kann.

## Begriffe

- **Telnyx FQDN Connection**: Telnyx SIP Connection (Credential Auth) + Routing
- **LiveKit SIP Trunks**:
  - Inbound Trunk: akzeptiert Telnyx → LiveKit
  - Outbound Trunk: LiveKit → Telnyx
- **Dispatch Rule**: legt fest, in welchen Room ein Inbound Call geroutet wird

## Step 1: Telnyx API Key

Setze lokal (nur für CLI/Setup-Skripte):

```bash
export TELNYX_API_KEY="..."
```

## Step 2: Telnyx FQDN Connection + FQDN

Erzeuge:

- Outbound Voice Profile
- FQDN Connection (Inbound + Outbound, Credential Auth)
- FQDN Mapping auf deinen LiveKit SIP Endpoint (z.B. `xxxx.sip.livekit.cloud:5060`)

## Step 3: Telnyx Nummer mit Connection verknüpfen

1) `phone_number_id` holen (E.164):

```bash
curl -L -g "https://api.telnyx.com/v2/phone_numbers?filter[phone_number]=+49..." \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TELNYX_API_KEY"
```

2) Nummer patchen:

```bash
curl -L -X PATCH "https://api.telnyx.com/v2/phone_numbers/<phone_number_id>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -H "Authorization: Bearer $TELNYX_API_KEY" \
  -d '{"id":"<phone_number_id>","connection_id":"<connection_id>"}'
```

## Step 4: LiveKit Outbound Trunk Header für Digest Auth

Setze im LiveKit Outbound Trunk (wichtig für Telnyx Digest Auth):

- Header: `X-Telnyx-Username=<username>`

In LiveKit CLI sichtbar in der “Headers” Spalte:

```bash
lk sip outbound-trunk list
```

## LiveKit: Trunks + Dispatch Rule

```bash
# Inbound trunk
lk sip inbound-trunk create --name <name> --numbers +49... --auth-user <user> --auth-pass <pass>

# Outbound trunk
lk sip outbound-trunk update --id <id> --name <name> --address sip.telnyx.com --numbers +49... --auth-user <user> --auth-pass <pass>

# Dispatch rule (Inbound -> Room)
lk sip dispatch-rule list
```

