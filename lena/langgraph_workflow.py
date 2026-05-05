from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages


class State(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def _respond(state: State) -> dict:
    last_user_text = ""
    for msg in reversed(state.get("messages", [])):
        if isinstance(msg, HumanMessage):
            last_user_text = msg.content if isinstance(msg.content, str) else str(msg.content)
            break

    # Minimal example workflow: deterministic response.
    # Replace this with real nodes/tools/LLM calls as needed.
    content = (
        "Hallo, hier ist Lena von step2job Berlin. "
        "Kurze Frage: Sprechen ich gerade mit der Person, die für Recruiting zuständig ist?"
    )
    if last_user_text:
        content = f"{content}\n\n(Dein letzter Satz war: {last_user_text})"

    return {"messages": [AIMessage(content=content)]}


def create_workflow():
    graph = StateGraph(State)
    graph.add_node("respond", _respond)
    graph.add_edge(START, "respond")
    graph.add_edge("respond", END)
    return graph.compile()

