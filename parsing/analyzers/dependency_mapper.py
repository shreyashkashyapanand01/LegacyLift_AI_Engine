import ast
import os
import logging
from typing import List, Dict
import javalang

logger = logging.getLogger(__name__)


# -------------------------
# Python Dependencies
# -------------------------
def extract_python_dependencies(file_path: str, base_path: str) -> List[Dict]:
    dependencies = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = ast.parse(source)

        relative_path = os.path.relpath(file_path, base_path).replace("\\", "/")

        for node in ast.walk(tree):

            # ✅ import math
            if isinstance(node, ast.Import):
                for alias in node.names:
                    logger.debug(f"Python import found: {alias.name}")

                    dependencies.append({
                        "from": relative_path,
                        "to": alias.name,
                        "type": "import",
                        "language": "python"
                    })

            # ✅ from os import path
            elif isinstance(node, ast.ImportFrom):
                if node.module:   # 🔥 FIX: avoid empty module
                    logger.debug(f"Python from-import found: {node.module}")

                    dependencies.append({
                        "from": relative_path,
                        "to": node.module,
                        "type": "import",
                        "language": "python"
                    })

        logger.info(f"Python dependencies extracted: {relative_path} -> {len(dependencies)}")

        return dependencies

    except SyntaxError:
        logger.warning(f"Python syntax error: {file_path}")
        return []

    except Exception:
        logger.exception(f"Failed to extract Python dependencies: {file_path}")
        return []


# -------------------------
# Java Dependencies
# -------------------------
def extract_java_dependencies(file_path: str, base_path: str) -> List[Dict]:
    dependencies = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source = f.read()

        tree = javalang.parse.parse(source)

        relative_path = os.path.relpath(file_path, base_path).replace("\\", "/")

        # 🔥 SAFE CHECK
        if hasattr(tree, "imports") and tree.imports:
            for imp in tree.imports:
                logger.debug(f"Java import found: {imp.path}")

                dependencies.append({
                    "from": relative_path,
                    "to": imp.path,
                    "type": "import",
                    "language": "java"
                })

        logger.info(f"Java dependencies extracted: {relative_path} -> {len(dependencies)}")

        return dependencies

    except javalang.parser.JavaSyntaxError:
        logger.warning(f"Java syntax error: {file_path}")
        return []

    except Exception:
        logger.exception(f"Failed to extract Java dependencies: {file_path}")
        return []


# -------------------------
# Unified Mapper
# -------------------------
def map_dependencies(root_path: str, files: List[Dict]) -> List[Dict]:
    all_dependencies = []

    logger.info("Starting dependency mapping")

    try:
        for file in files:
            relative_path = file["path"]
            language = file["language"]

            full_path = os.path.join(root_path, relative_path)

            if not os.path.exists(full_path):
                logger.warning(f"File not found during dependency mapping: {full_path}")
                continue

            if language == "python":
                deps = extract_python_dependencies(full_path, root_path)

            elif language == "java":
                deps = extract_java_dependencies(full_path, root_path)

            else:
                logger.debug(f"Skipping unsupported language: {language}")
                continue

            all_dependencies.extend(deps)

        logger.info(f"Dependency mapping completed: {len(all_dependencies)} dependencies")

        return all_dependencies

    except Exception:
        logger.exception("Dependency mapping failed")
        raise RuntimeError("Dependency mapping failed")