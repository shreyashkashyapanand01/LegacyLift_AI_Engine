import os
import pickle
import logging

import faiss

logger = logging.getLogger(__name__)


class IndexManager:
    def __init__(self, path: str):
        self.path = path
        self.index_path = os.path.join(path, "faiss.index")
        self.meta_path = os.path.join(path, "metadata.pkl")

    def save(self, index, metadata):
        try:
            logger.info("Saving FAISS index")

            faiss.write_index(index, self.index_path)

            with open(self.meta_path, "wb") as f:
                pickle.dump(metadata, f)

        except Exception:
            logger.exception("Failed to save index")
            raise RuntimeError("Index save failed")

    def load(self):
        try:
            logger.info("Loading FAISS index")

            index = faiss.read_index(self.index_path)

            with open(self.meta_path, "rb") as f:
                metadata = pickle.load(f)

            return index, metadata

        except Exception:
            logger.exception("Failed to load index")
            raise RuntimeError("Index load failed")