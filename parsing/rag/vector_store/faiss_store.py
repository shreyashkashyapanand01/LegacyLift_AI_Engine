# import logging
# import numpy as np
# import faiss

# logger = logging.getLogger(__name__)


# class FaissStore:
#     def __init__(self, dimension: int):
#         try:
#             logger.info(f"Initializing FAISS index with dim={dimension}")

#             self.dimension = dimension
#             self.index = faiss.IndexFlatIP(dimension)  # cosine similarity

#             # 🔥 Store FULL chunk (text + metadata)
#             self.data = []

#         except Exception:
#             logger.exception("Failed to initialize FAISS index")
#             raise RuntimeError("FAISS init failed")

#     # ---------------------------
#     # ➕ ADD
#     # ---------------------------
#     def add(self, vectors: np.ndarray, chunks: list):
#         """
#         vectors: np.ndarray
#         chunks: List[{
#             "text": str,
#             "metadata": dict
#         }]
#         """

#         try:
#             if len(vectors) != len(chunks):
#                 raise ValueError("Vectors and chunks size mismatch")

#             logger.info(f"Adding {len(vectors)} vectors to FAISS")

#             self.index.add(vectors)

#             # 🔥 Store full chunk (not just metadata)
#             self.data.extend(chunks)

#         except Exception:
#             logger.exception("Failed to add vectors to FAISS")
#             raise RuntimeError("FAISS add failed")

#     # ---------------------------
#     # 🔍 SEARCH
#     # ---------------------------
#     def search(self, query_vector: np.ndarray, top_k: int = 3):
#         """
#         Returns:
#         List of (score, chunk)
#         """

#         try:
#             logger.info(f"Searching top {top_k} similar chunks")

#             query_vector = np.expand_dims(query_vector, axis=0)

#             scores, indices = self.index.search(query_vector, top_k)

#             results = []

#             for score, idx in zip(scores[0], indices[0]):
#                 if idx == -1:
#                     continue

#                 chunk = self.data[idx]

#                 results.append(
#                     (
#                         float(score),
#                         chunk   # 🔥 full chunk (text + metadata)
#                     )
#                 )

#             return results

#         except Exception:
#             logger.exception("FAISS search failed")
#             raise RuntimeError("FAISS search failed")

import logging
import numpy as np
import faiss

logger = logging.getLogger(__name__)


class FaissStore:
    def __init__(self, dimension: int):
        try:
            logger.info(f"Initializing FAISS index with dim={dimension}")

            self.dimension = dimension
            self.index = faiss.IndexFlatIP(dimension)

            # 🔥 store full chunk
            self.data = []

        except Exception:
            logger.exception("Failed to initialize FAISS index")
            raise RuntimeError("FAISS init failed")

    # ---------------------------
    # ➕ ADD
    # ---------------------------
    def add(self, vectors: np.ndarray, chunks: list):
        try:
            if len(vectors) != len(chunks):
                raise ValueError("Vectors and chunks size mismatch")

            logger.info(f"Adding {len(vectors)} vectors to FAISS")

            self.index.add(vectors.astype("float32"))  # ✅ important
            self.data.extend(chunks)

        except Exception:
            logger.exception("Failed to add vectors to FAISS")
            raise RuntimeError("FAISS add failed")

    # ---------------------------
    # 🔍 SEARCH
    # ---------------------------
    def search(self, query_vector: np.ndarray, top_k: int = 3):
        try:
            logger.info(f"Searching top {top_k} similar chunks")

            query_vector = np.expand_dims(query_vector, axis=0).astype("float32")

            scores, indices = self.index.search(query_vector, top_k)

            results = []

            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue

                chunk = self.data[idx]

                results.append({
                    "score": float(score),
                    "text": chunk["text"],
                    "metadata": chunk["metadata"]
                })

            return results

        except Exception:
            logger.exception("FAISS search failed")
            raise RuntimeError("FAISS search failed")