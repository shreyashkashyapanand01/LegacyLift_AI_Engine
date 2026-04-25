import ast
import os
import logging
from typing import List, Dict
import javalang

from parsing.utils.path_utils import get_relative_path

logger = logging.getLogger(__name__)


# ---------------------------
# 🐍 PYTHON PARSER (GOOD)
# ---------------------------
def parse_python_file(file_path: str, base_path: str) -> List[Dict]:
    functions = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        tree = ast.parse(source_code)
        lines = source_code.splitlines()

        relative_path = get_relative_path(file_path, base_path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):

                start = node.lineno - 1
                end = getattr(node, "end_lineno", node.lineno)

                code_snippet = "\n".join(lines[start:end])

                function_data = {
                    "id": f"{relative_path}::{node.name}",
                    "name": node.name,
                    "file": relative_path,
                    "line": node.lineno,
                    "end_line": end,
                    "type": "function",
                    "language": "python",
                    "code": code_snippet
                }

                functions.append(function_data)

        logger.info(f"Parsed Python file: {file_path} -> {len(functions)} functions")
        return functions

    except SyntaxError:
        logger.warning(f"Syntax error in file: {file_path} -> Skipping")
        return []

    except Exception:
        logger.exception(f"Error parsing Python file: {file_path}")
        return []


# ---------------------------
# ☕ JAVA HELPER (🔥 NEW)
# ---------------------------
def _extract_java_method(lines, start_line):
    """
    Extract full Java method using brace matching
    """
    code_lines = []
    brace_count = 0
    started = False

    for i in range(start_line, len(lines)):
        line = lines[i]
        code_lines.append(line)

        brace_count += line.count("{")
        brace_count -= line.count("}")

        if "{" in line:
            started = True

        if started and brace_count == 0:
            break

    return "\n".join(code_lines)


# ---------------------------
# ☕ JAVA PARSER (FIXED)
# ---------------------------
def parse_java_file(file_path: str, base_path: str) -> List[Dict]:
    functions = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()

        lines = source_code.splitlines()
        tree = javalang.parse.parse(source_code)

        relative_path = get_relative_path(file_path, base_path)

        for _, node in tree:
            if isinstance(node, javalang.tree.MethodDeclaration):

                line_no = node.position.line if node.position else None
                start = (line_no - 1) if line_no else 0

                # ✅ FIXED extraction (NO MORE 10 lines)
                code_snippet = _extract_java_method(lines, start)

                function_data = {
                    "id": f"{relative_path}::{node.name}",
                    "name": node.name,
                    "file": relative_path,
                    "line": line_no,
                    "end_line": line_no,  # can improve later
                    "type": "method",
                    "language": "java",
                    "code": code_snippet
                }

                functions.append(function_data)

        logger.info(f"Parsed Java file: {file_path} -> {len(functions)} methods")
        return functions

    except javalang.parser.JavaSyntaxError:
        logger.warning(f"Java syntax error in file: {file_path} -> Skipping")
        return []

    except Exception:
        logger.exception(f"Error parsing Java file: {file_path}")
        return []