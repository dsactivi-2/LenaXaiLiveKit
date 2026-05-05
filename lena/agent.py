import os
from dotenv import load_dotenv
load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli

from livekit.plugins.xai import realtime as xai_realtime

from prompt import build_lena_sales_instructions
from realtime_settings import build_turn_detection
from orchestrator_graph import LangGraphOrchestrator
from livekit.agents.types import APIConnectOptions

try:
    from prometheus_client import Counter, start_http_server
except Exception:  # pragma: no cover
    Counter = None
    start_http_server = None

_KNOWN_VOICES = {"ara": "Ara", "eve": "Eve", "leo": "Leo", "rex": "Rex", "sal": "Sal"}

_PROM_STARTED = False
_TOOL_CALLS = Counter("lena_tool_calls_total", "Tool calls", ["tool"]) if Counter else None


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    raw = raw.strip().lower()
    if raw in {"1", "true", "yes", "y", "on"}:
        return True
    if raw in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _maybe_start_prometheus() -> None:
    global _PROM_STARTED
    if _PROM_STARTED:
        return
    if not _env_bool("PROMETHEUS_ENABLED", False):
        return
    if start_http_server is None:
        return
    port = int(os.getenv("PROMETHEUS_PORT", "8000") or "8000")
    start_http_server(port)
    _PROM_STARTED = True


def _get_voice() -> str:
    raw = os.getenv("LENA_XAI_VOICE") or os.getenv("XAI_VOICE") or "Ara"
    raw = raw.strip()
    if raw == "":
        return "Ara"
    return _KNOWN_VOICES.get(raw.lower(), raw)


def _get_model() -> str:
    return (os.getenv("LENA_XAI_MODEL") or os.getenv("XAI_MODEL") or "grok-voice-fast-1.0").strip()

def _get_int_env(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_float_env(name: str, default: float) -> float:
    raw = os.getenv(name)
    if raw is None or raw.strip() == "":
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_conn_options() -> APIConnectOptions:
    # Aliases to match common env naming
    max_retry = _get_int_env("XAI_MAX_RETRIES", _get_int_env("LENA_XAI_MAX_RETRIES", 3))
    timeout = _get_float_env("XAI_TIMEOUT", _get_float_env("LENA_XAI_TIMEOUT", 10.0))
    retry_interval = _get_float_env("XAI_RETRY_INTERVAL", _get_float_env("LENA_XAI_RETRY_INTERVAL", 2.0))
    return APIConnectOptions(max_retry=max_retry, timeout=timeout, retry_interval=retry_interval)


def _tooling_enabled() -> bool:
    return _env_bool("ENABLE_TOOL_CALLING", True)


def _web_search_enabled() -> bool:
    return _env_bool("ENABLE_WEB_SEARCH", False)


def _x_search_enabled() -> bool:
    return _env_bool("ENABLE_X_SEARCH", False)


class LenaAgent(Agent):
    def __init__(self):
        self._orchestrator = LangGraphOrchestrator()
        super().__init__(
            instructions=build_lena_sales_instructions(),
        )

    async def on_user_turn_completed(self, turn_ctx, new_message) -> None:
        if not self._orchestrator.enabled():
            return

        # Keep it fast: deterministic graph, no network/LLM calls.
        content_parts = getattr(new_message, "content", None) or []
        if isinstance(content_parts, str):
            user_text = content_parts
        else:
            user_text = " ".join([str(p) for p in content_parts])

        out = self._orchestrator.process(user_text)
        if out.hint:
            turn_ctx.add_message(
                role="system",
                content=f"ORCH({out.stage}): {out.hint}",
                extra={"lena_orchestrator": True, "stage": out.stage},
            )

    @agents.function_tool
    async def lookup_company(self, query: str) -> str:
        """Firmen-Infos/HR/kürzliche Job-Ads recherchieren."""
        if _TOOL_CALLS:
            _TOOL_CALLS.labels(tool="lookup_company").inc()
        if not _tooling_enabled():
            return "Tooling ist deaktiviert. Bitte frage stattdessen nach den Firmendaten oder bitte um eine E-Mail."
        return f"Für {query}: IT-Job auf Stepstone letzte Woche, HR: hr@firma.de, +49..."

    @agents.function_tool
    async def get_ad_package(self, platform: str) -> str:
        """Ad-Pakete/Preise."""
        if _TOOL_CALLS:
            _TOOL_CALLS.labels(tool="get_ad_package").inc()
        if not _tooling_enabled():
            return "Tooling ist deaktiviert. Bitte nenne die Pakete grob und biete an, Details per E-Mail zu senden."
        return f"{platform}: Basic 299€/Monat (150k Views), Premium 599€."

    @agents.function_tool
    async def web_search(self, query: str) -> str:
        """(Optional) Web-Suche nach Firmendaten. Muss separat integriert werden."""
        if _TOOL_CALLS:
            _TOOL_CALLS.labels(tool="web_search").inc()
        if not _web_search_enabled():
            return "Web-Suche ist deaktiviert."
        return (
            "Web-Suche ist aktiviert, aber noch nicht an einen Anbieter angebunden. "
            "Sag mir, welchen Provider du willst (z. B. Serper, Tavily) und gib mir den API-Key als Secret."
        )

    @agents.function_tool
    async def x_search(self, query: str) -> str:
        """(Optional) X/Twitter Suche. Muss separat integriert werden."""
        if _TOOL_CALLS:
            _TOOL_CALLS.labels(tool="x_search").inc()
        if not _x_search_enabled():
            return "X-Suche ist deaktiviert."
        return (
            "X-Suche ist aktiviert, aber noch nicht integriert. "
            "Wenn du Zugriff via X API oder 3rd-party willst, sag mir den Provider und gib mir den Key als Secret."
        )

async def entrypoint(ctx: JobContext):
    _maybe_start_prometheus()
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        llm=xai_realtime.RealtimeModel(
            api_key=os.getenv("XAI_API_KEY"),
            model=_get_model(),
            voice=_get_voice(),
            turn_detection=build_turn_detection(),
            conn_options=_get_conn_options(),
        )
    )

    await session.start(LenaAgent(), room=ctx.room)


def _prewarm(_: agents.JobProcess) -> None:
    # Optional: only available on Python 3.11+ (LiveKit Cloud uses 3.13).
    try:
        from livekit.agents import silero

        silero.VAD.load()
    except Exception:
        # Keep startup resilient on dev machines without silero deps.
        return


if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, prewarm_fnc=_prewarm, agent_name="lena"))
