import logging
import numpy as np
import faiss

logger = logging.getLogger(__name__)


class FaissStore:
    def __init__(self, dimension: int):
        try:
            logger.info(f"Initializing FAISS index with dim={dimension}")

            self.dimension = dimension
            self.index = faiss.IndexFlatIP(dimension)  # cosine similarity (after normalization)

            self.metadata = []  # store chunk metadata

        except Exception:
            logger.exception("Failed to initialize FAISS index")
            raise RuntimeError("FAISS init failed")

    def add(self, vectors: np.ndarray, metadata: list):
        """
        Add vectors + metadata
        """

        try:
            if len(vectors) != len(metadata):
                raise ValueError("Vectors and metadata size mismatch")

            logger.info(f"Adding {len(vectors)} vectors to FAISS")

            self.index.add(vectors)
            self.metadata.extend(metadata)

        except Exception:
            logger.exception("Failed to add vectors to FAISS")
            raise RuntimeError("FAISS add failed")

    def search(self, query_vector: np.ndarray, top_k: int = 3):
        """
        Search similar vectors
        """

        try:
            logger.info(f"Searching top {top_k} similar chunks")

            query_vector = np.expand_dims(query_vector, axis=0)

            scores, indices = self.index.search(query_vector, top_k)

            results = []

            for score, idx in zip(scores[0], indices[0]):
                if idx == -1:
                    continue

                results.append({
                    "score": float(score),
                    "metadata": self.metadata[idx]
                })

            return results

        except Exception:
            logger.exception("FAISS search failed")
            raise RuntimeError("FAISS search failed")