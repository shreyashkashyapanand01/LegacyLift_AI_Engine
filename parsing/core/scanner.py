import os
import logging
from typing import List, Dict

from parsing.config.settings import SUPPORTED_LANGUAGES
from parsing.utils.path_utils import get_relative_path

logger = logging.getLogger(__name__)

# 🚫 Ignore directories
IGNORED_DIRS = {
    ".git",
    "__pycache__",
    "node_modules",
    ".idea",
    ".vscode"
}


def scan_project(root_path: str) -> List[Dict]:
    """
    Scans a project directory and returns list of code files with metadata.
    """

    if not os.path.exists(root_path):
        logger.error(f"Path does not exist: {root_path}")
        raise ValueError("Invalid path")

    if not os.path.isdir(root_path):
        logger.error(f"Path is not a directory: {root_path}")
        raise ValueError("Path must be a directory")

    logger.info(f"Starting scan for: {root_path}")

    results = []

    try:
        for current_root, dirs, files in os.walk(root_path):

            # 🔥 Remove ignored directories
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for file in files:
                ext = os.path.splitext(file)[1].lower()

                if ext not in SUPPORTED_LANGUAGES:
                    continue

                full_path = os.path.join(current_root, file)

                # ✅ Use centralized path logic
                normalized_path = get_relative_path(full_path, root_path)

                file_data = {
                    "path": normalized_path,
                    "language": SUPPORTED_LANGUAGES[ext]
                }

                results.append(file_data)

                logger.debug(f"Found file: {normalized_path}")

        logger.info(f"Scan completed. Total files found: {len(results)}")

        return results

    except Exception:
        logger.exception("Error during scanning")
        raise RuntimeError("Scanning failed")