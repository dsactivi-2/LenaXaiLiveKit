import os
from dotenv import load_dotenv
load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli

from livekit.plugins.xai import realtime as xai_realtime

from prompt import build_lena_sales_instructions
from realtime_settings import build_turn_detection

class LenaAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions=build_lena_sales_instructions(),
        )

    @agents.function_tool
    async def lookup_company(self, query: str) -> str:
        """Firmen-Infos/HR/kürzliche Job-Ads recherchieren."""
        return f"Für {query}: IT-Job auf Stepstone letzte Woche, HR: hr@firma.de, +49..."

    @agents.function_tool
    async def get_ad_package(self, platform: str) -> str:
        """Ad-Pakete/Preise."""
        return f"{platform}: Basic 299€/Monat (150k Views), Premium 599€."

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=agents.AutoSubscribe.AUDIO_ONLY)

    session = AgentSession(
        llm=xai_realtime.RealtimeModel(
            api_key=os.getenv("XAI_API_KEY"),
            model=os.getenv("LENA_XAI_MODEL", "grok-voice-fast-1.0"),
            voice=os.getenv("LENA_XAI_VOICE", "Ara"),
            turn_detection=build_turn_detection(),
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
