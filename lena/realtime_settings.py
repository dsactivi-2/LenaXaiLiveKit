import os

from livekit.plugins.xai.realtime import TurnDetection


def _get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    return default if value is None or value.strip() == "" else value.strip()


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return float(value)
    except ValueError:
        return default


def _get_env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    value = value.strip().lower()
    if value in {"1", "true", "yes", "y", "on"}:
        return True
    if value in {"0", "false", "no", "n", "off"}:
        return False
    return default


def build_turn_detection() -> TurnDetection:
    """
    Turn detection tuning for telephony.

    Defaults are intentionally conservative for PSTN/SIP:
    - Short prefix padding to avoid clipping the first phonemes
    - Moderate silence to avoid talking over users
    - Interrupt enabled so barge-in works
    """
    td_type = _get_env_str("LENA_TURN_DETECTION_TYPE", _get_env_str("TURN_DETECTION", "server_vad"))
    eagerness = _get_env_str("LENA_TURN_EAGERNESS", "medium")

    return TurnDetection(
        type=td_type,  # "server_vad" or "semantic_vad"
        threshold=_get_env_float("LENA_TURN_THRESHOLD", _get_env_float("VAD_THRESHOLD", 0.5)),
        prefix_padding_ms=_get_env_int("LENA_TURN_PREFIX_PADDING_MS", _get_env_int("PREFIX_PADDING_MS", 160)),
        silence_duration_ms=_get_env_int(
            "LENA_TURN_SILENCE_DURATION_MS", _get_env_int("SILENCE_DURATION_MS", 520)
        ),
        interrupt_response=_get_env_bool("LENA_TURN_INTERRUPT_RESPONSE", True),
        create_response=_get_env_bool("LENA_TURN_CREATE_RESPONSE", True),
        eagerness=eagerness,  # "low" | "medium" | "high" | "auto"
    )
