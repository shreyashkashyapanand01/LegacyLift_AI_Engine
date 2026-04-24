import json
import os
import logging
from typing import Any

logger = logging.getLogger(__name__)


def write_json(file_path: str, data: Any):
    """
    Writes JSON data to a file with proper formatting.
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        logger.info(f"JSON written to: {file_path}")

    except Exception:
        logger.exception(f"Failed to write JSON: {file_path}")
        raise RuntimeError("JSON write failed")


def read_json(file_path: str) -> Any:
    """
    Reads JSON data from a file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        logger.exception(f"Failed to read JSON: {file_path}")
        raise RuntimeError("JSON read failed")