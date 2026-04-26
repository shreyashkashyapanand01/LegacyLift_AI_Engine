# import logging
# from typing import List, Dict
# import re

# logger = logging.getLogger(__name__)


# class Retriever:
#     def __init__(self, store, embedder):
#         self.store = store
#         self.embedder = embedder

#     # ---------------------------
#     # 🔍 QUERY ANALYSIS
#     # ---------------------------
#     def _detect_language(self, query: str):
#         query = query.lower()

#         if "python" in query:
#             return "python"
#         elif "java" in query:
#             return "java"

#         return None

#     def _extract_keywords(self, text: str):
#         return set(re.findall(r"\b\w+\b", text.lower()))

#     # ---------------------------
#     # ⚖️ HYBRID SCORING (IMPROVED)
#     # ---------------------------
#     def _score(self, query, chunk, base_score):
#         text = chunk["text"]
#         metadata = chunk["metadata"]

#         query_words = self._extract_keywords(query)
#         text_words = self._extract_keywords(text)

#         # 🔹 keyword overlap
#         overlap = len(query_words & text_words)
#         keyword_score = overlap / (len(query_words) + 1)

#         # 🔹 function match boost (stronger now)
#         func_name = metadata.get("function", "").lower()
#         func_score = 1.0 if func_name and func_name in query.lower() else 0.0

#         # 🔥 improved weighting
#         final_score = (
#             0.6 * base_score +
#             0.25 * keyword_score +
#             0.15 * func_score
#         )

#         return final_score

#     # ---------------------------
#     # 🚀 RETRIEVE
#     # ---------------------------
#     def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
#         try:
#             logger.info(f"Retrieving for query: {query}")

#             language_filter = self._detect_language(query)

#             query_vector = self.embedder.embed_query(query)

#             raw_results = self.store.search(query_vector, top_k * 3)

#             scored_results = []

#             for r in raw_results:
#                 base_score = r["score"]
#                 chunk = {
#                     "text": r["text"],
#                     "metadata": r["metadata"]
#                 }

#                 metadata = chunk["metadata"]

#                 # 🔹 language filter
#                 if language_filter:
#                     if metadata.get("language") != language_filter:
#                         continue

#                 final_score = self._score(query, chunk, base_score)

#                 scored_results.append((final_score, chunk))

#             # 🔹 sort
#             scored_results.sort(key=lambda x: x[0], reverse=True)

#             # 🔹 deduplicate
#             seen = set()
#             final_results = []

#             for score, chunk in scored_results:
#                 cid = chunk["metadata"]["id"]

#                 if cid in seen:
#                     continue

#                 seen.add(cid)

#                 final_results.append({
#                     "score": score,
#                     "code": chunk["text"],
#                     "file": chunk["metadata"]["file"],
#                     "function": chunk["metadata"].get("function"),
#                     "language": chunk["metadata"].get("language")
#                 })

#                 if len(final_results) >= top_k:
#                     break

#             logger.info(f"Retrieved {len(final_results)} results")

#             return final_results

#         except Exception:
#             logger.exception("Retrieval failed")
#             raise RuntimeError("Retriever failed")

#     # ---------------------------
#     # 🧠 CONTEXT BUILDER (UPGRADED 🔥)
#     # ---------------------------
#     def build_context(self, results: List[Dict]) -> str:
#         try:
#             blocks = []

#             for r in results:
#                 block = f"""
# File: {r["file"]}
# Function: {r["function"]}
# Language: {r["language"]}

# Code:
# {r["code"]}
# """
#                 blocks.append(block.strip())

#             return "\n\n".join(blocks)

#         except Exception:
#             logger.exception("Context building failed")
#             raise RuntimeError("Context build failed")




import logging
from typing import List, Dict
import re

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, store, embedder):
        self.store = store
        self.embedder = embedder

    # ---------------------------
    # 🔍 QUERY ANALYSIS
    # ---------------------------
    def _detect_language(self, query: str):
        query = query.lower()

        if "python" in query:
            return "python"
        elif "java" in query:
            return "java"

        return None

    def _extract_keywords(self, text: str):
        return set(re.findall(r"\b\w+\b", text.lower()))

    # 🔥 NEW: detect target function
    def _extract_function_name(self, query: str):
        words = query.lower().split()

        for i, w in enumerate(words):
            if w == "function" and i > 0:
                return words[i - 1]  # word before "function"

        return None

    # ---------------------------
    # ⚖️ HYBRID SCORING (IMPROVED)
    # ---------------------------
    def _score(self, query, chunk, base_score):
        text = chunk["text"]
        metadata = chunk["metadata"]

        query_words = self._extract_keywords(query)
        text_words = self._extract_keywords(text)

        # keyword overlap
        overlap = len(query_words & text_words)
        keyword_score = overlap / (len(query_words) + 1)

        # 🔥 stronger function match
        func_name = metadata.get("function", "").lower()

        if func_name and func_name in query.lower():
            func_score = 2.0   # 🔥 boosted
        else:
            func_score = 0.0

        final_score = (
            0.55 * base_score +
            0.25 * keyword_score +
            0.20 * func_score
        )

        return final_score

    # ---------------------------
    # 🚀 RETRIEVE (PRECISION FIXED)
    # ---------------------------
    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        try:
            logger.info(f"Retrieving for query: {query}")

            language_filter = self._detect_language(query)
            target_function = self._extract_function_name(query)

            query_vector = self.embedder.embed_query(query)

            raw_results = self.store.search(query_vector, top_k * 5)

            scored_results = []

            for r in raw_results:
                base_score = r["score"]
                chunk = {
                    "text": r["text"],
                    "metadata": r["metadata"]
                }

                metadata = chunk["metadata"]

                # 🔹 language filter
                if language_filter:
                    if metadata.get("language") != language_filter:
                        continue

                func_name = metadata.get("function", "").lower()

                # 🔥 HARD FILTER (only when function clearly specified)
                if target_function:
                    if func_name != target_function:
                        continue

                final_score = self._score(query, chunk, base_score)

                scored_results.append((final_score, chunk))

            # 🔹 sort
            scored_results.sort(key=lambda x: x[0], reverse=True)

            # 🔹 deduplicate
            seen = set()
            final_results = []

            for score, chunk in scored_results:
                metadata = chunk["metadata"]
                cid = metadata["id"]

                if cid in seen:
                    continue

                seen.add(cid)

                final_results.append({
                    "score": score,
                    "code": chunk["text"],
                    "file": metadata["file"],
                    "function": metadata.get("function"),
                    "language": metadata.get("language")
                })

                if len(final_results) >= top_k:
                    break

            logger.info(f"Retrieved {len(final_results)} results")

            return final_results

        except Exception:
            logger.exception("Retrieval failed")
            raise RuntimeError("Retriever failed")

    # ---------------------------
    # 🧠 CONTEXT BUILDER (CLEAN)
    # ---------------------------
    def build_context(self, results: List[Dict]) -> str:
        try:
            blocks = []

            for r in results:
                block = f"""
File: {r["file"]}
Function: {r["function"]}
Language: {r["language"]}

Code:
{r["code"]}
"""
                blocks.append(block.strip())

            return "\n\n".join(blocks)

        except Exception:
            logger.exception("Context building failed")
            raise RuntimeError("Context build failed")