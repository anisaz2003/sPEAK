import json
import os

DEFAULTS = {
    "model_size": "base",
    "language": None,
    "device": "cpu",
    "compute_type": "int8",
    "hotkey": "ctrl+windows",
    "sample_rate": 16000,
    "notifications": True,
    "beam_size": 5,
    "vad_filter": True,
}


def load_config(path: str) -> dict:
    config = dict(DEFAULTS)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            user = json.load(f)
        config.update({k: v for k, v in user.items() if v is not None or k == "language"})
    return config
