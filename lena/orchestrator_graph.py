import os
from dataclasses import dataclass

from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


@dataclass
class OrchestratorOutput:
    stage: str
    hint: str


def _norm(text: str) -> str:
    return (text or "").strip().lower()


def _contains_any(text: str, needles: list[str]) -> bool:
    t = _norm(text)
    return any(n in t for n in needles)


def create_orchestrator_graph():
    """
    A fast, deterministic LangGraph used as a sidecar orchestrator.

    Important: no network calls, no external LLM calls. This keeps latency negligible and
    works well alongside a realtime voice model.
    """

    def route(state: dict) -> dict:
        user_text = state.get("user_text", "")
        stage = state.get("stage", "intro")

        if _contains_any(
            user_text,
            [
                "nicht anrufen",
                "nicht mehr anrufen",
                "rausnehmen",
                "opt out",
                "opt-out",
                "keine werbung",
            ],
        ):
            return {"stage": "optout", "hint": "OPT-OUT: Sofort entschuldigen, Opt-out bestätigen, Gespräch beenden."}

        if _contains_any(user_text, ["keine zeit", "gerade schlecht", "später", "rufen sie später", "rufen sie später an"]):
            return {"stage": "reschedule", "hint": "Kurz halten: 1 Satz + konkreten Termin-Vorschlag (2 Slots)."}

        if _contains_any(user_text, ["kein budget", "zu teuer", "budget", "kosten", "preis"]):
            return {"stage": "objection_budget", "hint": "Einwand Budget: nach Dringlichkeit/Kosten unbesetzter Stelle fragen, dann Mini-Pitch."}

        if _contains_any(user_text, ["haben schon", "bereits", "agentur", "anbietern", "anbieter", "intern", "inhouse"]):
            return {"stage": "objection_existing", "hint": "Einwand Anbieter: 'Was läuft gut – was soll besser werden?' dann Termin anbieten."}

        if stage in {"intro"}:
            return {"stage": "qualify", "hint": "Qualify: Rolle/Bedarf (Rollen, Anzahl, Timeline) in 1–2 Fragen."}

        if stage in {"qualify"}:
            return {"stage": "pitch", "hint": "Pitch: 2 Sätze Nutzen + 1 Frage, dann Termin (2 Slots)."}

        if stage in {"pitch"}:
            return {"stage": "close", "hint": "Close: Terminfrage; bei Nein: Erlaubnis Follow-up + E-Mail."}

        return {"stage": stage, "hint": "Kurz, 1 Frage pro Turn; Ziel: Termin."}

    workflow = StateGraph(dict)
    workflow.add_node("route", route)
    workflow.add_edge(START, "route")
    workflow.add_edge("route", END)
    return workflow.compile()


class LangGraphOrchestrator:
    def __init__(self) -> None:
        self._graph = create_orchestrator_graph()
        self._stage = "intro"

    def enabled(self) -> bool:
        raw = os.getenv("ENABLE_LANGGRAPH_ORCHESTRATOR")
        if raw is None:
            # Default to enabled for sidecar mode.
            return True
        raw = raw.strip().lower()
        if raw in {"1", "true", "yes", "y", "on"}:
            return True
        if raw in {"0", "false", "no", "n", "off"}:
            return False
        return True

    def process(self, user_text: str) -> OrchestratorOutput:
        result = self._graph.invoke({"user_text": user_text, "stage": self._stage})
        self._stage = result.get("stage", self._stage)
        return OrchestratorOutput(stage=self._stage, hint=result.get("hint", "").strip())
