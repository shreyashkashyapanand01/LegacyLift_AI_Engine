import logging
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from huggingface_hub import login

from parsing.config.settings import EMBEDDING_MODEL, DEVICE, HF_TOKEN

logger = logging.getLogger(__name__)


class Embedder:
    def __init__(self):
        try:
            logger.info(f"Loading embedding model: {EMBEDDING_MODEL}")

            # 🔥 Authenticate once (no deprecated usage)
            if HF_TOKEN:
                login(token=HF_TOKEN)
                logger.info("HF token authenticated")

            # 🔥 Load model (no token passed here)
            self.model = SentenceTransformer(
                EMBEDDING_MODEL,
                device=DEVICE
            )

            logger.info("Embedding model loaded successfully")

        except Exception:
            logger.exception("Failed to load embedding model")
            raise RuntimeError("Embedding model initialization failed")

    def embed_documents(self, texts: List[str]) -> np.ndarray:
        """
        Converts list of texts -> embeddings
        """

        try:
            logger.info(f"Generating embeddings for {len(texts)} chunks")

            embeddings = self.model.encode(
                texts,
                batch_size=32,
                show_progress_bar=True,
                normalize_embeddings=True  # 🔥 critical for cosine similarity
            )

            return embeddings

        except Exception:
            logger.exception("Embedding generation failed")
            raise RuntimeError("Embedding failed")

    def embed_query(self, query: str) -> np.ndarray:
        """
        Embeds a single query
        """

        try:
            embedding = self.model.encode(
                [query],
                normalize_embeddings=True
            )

            return embedding[0]

        except Exception:
            logger.exception("Query embedding failed")
            raise RuntimeError("Query embedding failed")