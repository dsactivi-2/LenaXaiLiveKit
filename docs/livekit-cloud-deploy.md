# LiveKit Cloud Deploy

## Voraussetzungen

- LiveKit CLI installiert: `lk --version`
- LiveKit Cloud Zugang (Projekt/Subdomain + API Key/Secret)

## Deploy (neu)

```bash
cd lena
lk cloud auth
lk agent create --region eu-central --secrets-file secrets.env .
```

## Deploy (Update)

```bash
cd lena
lk agent deploy --region eu-central --secrets-file secrets.env .
```

## Status & Logs

```bash
cd lena
lk agent status
lk agent logs --log-type=deploy
lk agent logs --log-type=build
```

## Secrets setzen / rotieren

```bash
cd lena
lk agent update-secrets --secrets KEY=VALUE
lk agent secrets
```

