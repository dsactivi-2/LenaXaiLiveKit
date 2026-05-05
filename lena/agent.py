import os
from dotenv import load_dotenv
load_dotenv()

from livekit import agents
from livekit.agents import AgentSession, Agent, JobContext, WorkerOptions, cli

from livekit.plugins import langchain as lk_langchain

from langgraph_workflow import create_workflow

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

    session = AgentSession(llm=lk_langchain.LLMAdapter(graph=create_workflow()))

    await session.start(LenaAgent(), room=ctx.room)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint, agent_name="lena"))
