import ast
import os
import logging
from typing import List, Dict
import javalang

from parsing.utils.path_utils import get_relative_path

logger = logging.getLogger(__name__)


def parse_python_file(file_path: str, base_path: str) -> List[Dict]:
    """
    Parses a Python file and extracts function definitions.
    """

    functions = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)

        # ✅ Compute once
        relative_path = get_relative_path(file_path, base_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):

                function_data = {
                    "id": f"{relative_path}::{node.name}",
                    "name": node.name,
                    "file": relative_path,
                    "line": node.lineno,
                    "end_line": getattr(node, "end_lineno", node.lineno),
                    "type": "function",
                    "language": "python"
                }

                functions.append(function_data)

                logger.debug(f"Found function: {node.name} in {relative_path}")

        logger.info(f"Parsed Python file: {file_path} -> {len(functions)} functions")

        return functions

    except SyntaxError:
        logger.warning(f"Syntax error in file: {file_path} -> Skipping")
        return []

    except Exception:
        logger.exception(f"Error parsing Python file: {file_path}")
        return []


def parse_java_file(file_path: str, base_path: str) -> List[Dict]:
    """
    Parses a Java file and extracts method declarations.
    """

    functions = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = javalang.parse.parse(source_code)

        # ✅ Compute once
        relative_path = get_relative_path(file_path, base_path)

        for _, node in tree:
            if isinstance(node, javalang.tree.MethodDeclaration):

                line_no = node.position.line if node.position else None

                function_data = {
                    "id": f"{relative_path}::{node.name}",
                    "name": node.name,
                    "file": relative_path,
                    "line": line_no,
                    "end_line": line_no,  # limitation (acceptable for now)
                    "type": "method",
                    "language": "java"
                }

                functions.append(function_data)

                logger.debug(f"Found Java method: {node.name} in {relative_path}")

        logger.info(f"Parsed Java file: {file_path} -> {len(functions)} methods")

        return functions

    except javalang.parser.JavaSyntaxError:
        logger.warning(f"Java syntax error in file: {file_path} -> Skipping")
        return []

    except Exception:
        logger.exception(f"Error parsing Java file: {file_path}")
        return []