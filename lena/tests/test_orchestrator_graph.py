from orchestrator_graph import LangGraphOrchestrator


def test_optout_detection() -> None:
    orch = LangGraphOrchestrator()
    out = orch.process("Bitte nehmen Sie mich raus, nicht mehr anrufen.")
    assert out.stage == "optout"
    assert "OPT-OUT" in out.hint


def test_budget_objection_routing() -> None:
    orch = LangGraphOrchestrator()
    out = orch.process("Dafür haben wir leider kein Budget, zu teuer.")
    assert out.stage == "objection_budget"
    assert "Budget" in out.hint

