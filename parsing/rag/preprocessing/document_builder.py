# import os
# import logging
# from typing import List, Dict

# from parsing.utils.path_utils import normalize_path

# logger = logging.getLogger(__name__)


# def build_documents(parsed_output: Dict, root_path: str) -> List[Dict]:
#     """
#     Converts parsed JSON → list of documents (text + metadata)

#     Args:
#         parsed_output: output.json data from Module 1
#         root_path: absolute path to project root

#     Returns:
#         List of documents for embedding
#     """

#     documents = []

#     try:
#         functions = parsed_output.get("functions", [])

#         for func in functions:
#             file_path = func["file"]

#             # 🔥 Build absolute path
#             full_path = os.path.join(root_path, file_path)

#             if not os.path.exists(full_path):
#                 logger.warning(f"File not found: {full_path}")
#                 continue

#             # 🔥 Extract code snippet
#             code_snippet = _extract_code_snippet(
#                 full_path,
#                 func["line"],
#                 func["end_line"]
#             )

#             if not code_snippet.strip():
#                 continue

#             doc = {
#                 "text": code_snippet,
#                 "metadata": {
#                     "id": func["id"],
#                     "file": normalize_path(file_path),
#                     "function": func["name"],
#                     "language": func["language"],
#                     "start_line": func["line"],
#                     "end_line": func["end_line"]
#                 }
#             }

#             documents.append(doc)

#         logger.info(f"Built {len(documents)} documents from parsed output")

#         return documents

#     except Exception:
#         logger.exception("Failed to build documents")
#         raise RuntimeError("Document building failed")


# def _extract_code_snippet(file_path: str, start_line: int, end_line: int) -> str:
#     """
#     Extracts code snippet from file using line numbers
#     """

#     try:
#         with open(file_path, "r", encoding="utf-8") as f:
#             lines = f.readlines()

#         # Python uses 0-index internally
#         snippet = lines[start_line - 1:end_line]

#         return "".join(snippet)

#     except Exception:
#         logger.exception(f"Failed to extract snippet from {file_path}")
#         return ""



import logging
from typing import List, Dict

from parsing.utils.path_utils import normalize_path

logger = logging.getLogger(__name__)


def build_documents(parsed_output: Dict, root_path: str) -> List[Dict]:
    """
    Converts parsed JSON -> documents for RAG
    """

    documents = []

    try:
        functions = parsed_output.get("functions", [])

        for func in functions:

            # 🔥 FIX 1: schema compatibility
            function_name = func.get("function") or func.get("name", "")

            # 🔥 FIX 2: use parser-provided code (FAST + CORRECT)
            code_snippet = func.get("code", "")

            if not code_snippet.strip():
                continue

            doc = {
                "text": code_snippet,
                "metadata": {
                    "id": func.get("id"),
                    "file": normalize_path(func.get("file")),
                    "function": function_name,
                    "language": func.get("language"),
                    "start_line": func.get("line"),
                    "end_line": func.get("end_line")
                }
            }

            documents.append(doc)

        logger.info(f"Built {len(documents)} documents from parsed output")

        return documents

    except Exception:
        logger.exception("Failed to build documents")
        raise RuntimeError("Document building failed")