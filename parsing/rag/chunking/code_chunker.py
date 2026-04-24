import os
import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


MIN_LINES = 3
MAX_LINES = 50


def chunk_documents(documents: List[Dict], root_path: str) -> List[Dict]:
    """
    Enhances documents into better chunks for RAG

    Args:
        documents: output from document_builder
        root_path: project root path

    Returns:
        Improved chunks
    """

    chunks = []

    try:
        for doc in documents:
            text = doc["text"]
            metadata = doc["metadata"]

            line_count = text.count("\n") + 1

            # 🔥 Strategy 1: Expand small chunks
            if line_count < MIN_LINES:
                expanded_text = _expand_chunk(metadata, root_path)

                if expanded_text:
                    doc["text"] = expanded_text

            # 🔥 Strategy 2: Limit max size
            doc["text"] = _limit_chunk_size(doc["text"])

            chunks.append(doc)

        logger.info(f"Chunking completed: {len(chunks)} chunks")

        return chunks

    except Exception:
        logger.exception("Chunking failed")
        raise RuntimeError("Chunking failed")


# -------------------------
# Helpers
# -------------------------

def _expand_chunk(metadata: Dict, root_path: str) -> str:
    """
    Expands chunk using brace matching (better accuracy)
    """

    try:
        file_path = metadata["file"]
        start = metadata["start_line"]

        full_path = os.path.join(root_path, file_path)

        if not os.path.exists(full_path):
            return ""

        with open(full_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        snippet = []
        brace_count = 0
        started = False

        for i in range(start - 1, len(lines)):
            line = lines[i]
            snippet.append(line)

            # Count braces
            brace_count += line.count("{")
            brace_count -= line.count("}")

            # Mark when function actually starts
            if "{" in line:
                started = True

            # Stop when function closes
            if started and brace_count <= 0:
                break

            # safety limit
            if len(snippet) > 50:
                break

        return "".join(snippet)

    except Exception:
        logger.warning(f"Failed to expand chunk: {metadata.get('id')}")
        return ""

def _limit_chunk_size(text: str) -> str:
    """
    Limits chunk size to avoid oversized embeddings
    """

    lines = text.splitlines()

    if len(lines) > MAX_LINES:
        return "\n".join(lines[:MAX_LINES])

    return text