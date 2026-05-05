import sys
from pathlib import Path


# Allow tests to import the local module files (agent.py, realtime_settings.py, etc.)
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

