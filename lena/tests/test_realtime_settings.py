import os

from realtime_settings import build_turn_detection


def test_turn_detection_env_aliases(monkeypatch) -> None:
    monkeypatch.setenv("TURN_DETECTION", "server_vad")
    monkeypatch.setenv("VAD_THRESHOLD", "0.4")
    monkeypatch.setenv("PREFIX_PADDING_MS", "400")
    monkeypatch.setenv("SILENCE_DURATION_MS", "250")

    td = build_turn_detection()
    assert td.type == "server_vad"
    assert td.threshold == 0.4
    assert td.prefix_padding_ms == 400
    assert td.silence_duration_ms == 250


def test_turn_detection_overrides_aliases(monkeypatch) -> None:
    monkeypatch.setenv("TURN_DETECTION", "server_vad")
    monkeypatch.setenv("VAD_THRESHOLD", "0.4")

    monkeypatch.setenv("LENA_TURN_THRESHOLD", "0.55")
    td = build_turn_detection()
    assert td.threshold == 0.55

