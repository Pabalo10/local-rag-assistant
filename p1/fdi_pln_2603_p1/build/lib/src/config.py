from __future__ import annotations
import os

MI_ALIAS = "Nortenios"
MODEL_NAME = "qwen3:8b"
OLLAMA_URL = "http://localhost:11434/api/generate"

try:
    BUTLER_ADDRESS = os.environ["FDI_PLN__BUTLER_ADDRESS"]
except KeyError as exc:
    raise RuntimeError(
        "La variable de entorno FDI_PLN__BUTLER_ADDRESS no está definida."
    ) from exc
