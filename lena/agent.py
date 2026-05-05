import os
from dotenv import load_dotenv
load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli
from livekit.plugins import xai

class LenaAgent(Agent):
    def __init__(self):
        super().__init__(
            instructions="""Du bist Lena von step2job Berlin. Freundliche Sales-Rep. Rufst HR-Firmen an, die kürzlich Jobs auf Stepstone/Indeed ausschrieben haben, upsellst weitere Ads.

Hook: 'Guten Tag, hier ist Lena von step2job in Berlin. Ich habe gesehen, dass Sie kürzlich eine Stelle als [Job] ausgeschrieben haben...'

Tools priorisieren: lookup_company, get_ad_package. Pitch Reichweite/Pakete (299€+), ROI-Einwände, Abschluss/Follow-up.
DSGVO: Nur öffentliche Daten. Natürliches, flüssiges Deutsch, enthusiastisch, empathisch – respektiere 'Nein'.""",
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
        llm=xai.realtime.RealtimeModel(
            api_key=os.environ["XAI_API_KEY"],
            model="grok-voice-think-fast-1.0",
            voice="sal",  # Männlich, professionell – deine Wahl!
            turn_detection={
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 300,
                "silence_duration_ms": 800,
            },
        ),
    )
    
    await session.start(ctx.room, agent=LenaAgent())

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))

