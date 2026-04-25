import logging
from typing import List, Dict

from parsing.rag.embedding.embedder import Embedder
from parsing.rag.vector_store.faiss_store import FaissStore

logger = logging.getLogger(__name__)


class Retriever:
    def __init__(self, store: FaissStore, embedder: Embedder):
        self.store = store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 3) -> List[Dict]:
        """
        Main retrieval function
        """

        try:
            logger.info(f"Retrieving for query: {query}")

            # 🔥 Step 1: embed query
            query_vector = self.embedder.embed_query(query)

            # 🔥 Step 2: search FAISS
            results = self.store.search(query_vector, top_k)

            # 🔥 Step 3: format results
            formatted_results = []

            for r in results:
                metadata = r["metadata"]

                formatted_results.append({
                    "score": r["score"],
                    "code": metadata["text"],
                    "file": metadata["metadata"]["file"],
                    "function": metadata["metadata"]["function"],
                    "language": metadata["metadata"]["language"]
                })

            logger.info(f"Retrieved {len(formatted_results)} results")

            return formatted_results

        except Exception:
            logger.exception("Retrieval failed")
            raise RuntimeError("Retriever failed")

    def build_context(self, results: List[Dict]) -> str:
        """
        Combine retrieved chunks into a single context string
        """

        try:
            context = "\n\n".join([r["code"] for r in results])
            return context

        except Exception:
            logger.exception("Context building failed")
            raise RuntimeError("Context build failed")