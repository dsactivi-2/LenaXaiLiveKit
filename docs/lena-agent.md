# Lena Agent (DE) – Architektur

## Komponenten

- **LiveKit Agents Worker** (`lena/agent.py`)
  - verbindet sich in einen LiveKit Room (Audio only)
  - startet eine `AgentSession` mit `livekit.plugins.xai` Realtime Model
- **LLM / Voice**
  - xAI Realtime Model (Model + Voice + VAD im Code konfiguriert)
- **Tools**
  - Beispiel-Tools via `@agents.function_tool` (Demo: `lookup_company`, `get_ad_package`)

## Event-/Audio-Flow (hochlevel)

1. Worker startet in LiveKit Cloud oder lokal (`uv run agent.py dev`)
2. `entrypoint()` verbindet sich in den Room
3. `AgentSession.start()` hängt den Agent an den Room
4. Realtime Model erzeugt Audio + Tool Calls, LiveKit streamt Audio

## Konfig-Quellen

- `.env` lokal (via `python-dotenv`)
- LiveKit Cloud Agent Secrets (Env Vars im Container)

Siehe `docs/security-secrets.md` für Best Practices.

