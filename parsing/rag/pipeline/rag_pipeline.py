import os
import logging
from typing import Dict

from parsing.core.scanner import scan_project
from parsing.core.orchestrator import run_pipeline

from parsing.rag.preprocessing.document_builder import build_documents
from parsing.rag.chunking.code_chunker import chunk_documents
from parsing.rag.embedding.embedder import Embedder
from parsing.rag.vector_store.faiss_store import FaissStore
from parsing.rag.vector_store.index_manager import IndexManager
from parsing.rag.retrieval.retriever import Retriever

logger = logging.getLogger(__name__)


class RAGPipeline:
    def __init__(self, index_dir: str):
        self.index_dir = index_dir
        os.makedirs(index_dir, exist_ok=True)

        self.embedder = Embedder()
        self.index_manager = IndexManager(index_dir)

        self.store = None
        self.retriever = None

    # ---------------------------
    # INDEXING PHASE
    # ---------------------------
    def build_index(self, root_path: str):
        """
        code -> parse -> chunk -> embed -> FAISS -> save
        """

        try:
            logger.info("Starting RAG indexing pipeline")

            # Module 1
            files = scan_project(root_path)
            parsed_output = run_pipeline(root_path, files)

            # Module 2
            docs = build_documents(parsed_output, root_path)
            chunks = chunk_documents(docs, root_path)

            texts = [c["text"] for c in chunks]

            # Embeddings
            vectors = self.embedder.embed_documents(texts)

            # FAISS
            dim = vectors.shape[1]
            self.store = FaissStore(dim)
            self.store.add(vectors, chunks)

            # ✅ FIX: save FULL chunk data (not metadata)
            self.index_manager.save(self.store.index, self.store.data)

            logger.info("Index built and saved successfully")

        except Exception:
            logger.exception("Indexing failed")
            raise RuntimeError("RAG indexing failed")

    # ---------------------------
    # LOAD INDEX
    # ---------------------------
    def load_index(self):
        """
        Load FAISS index
        """

        try:
            logger.info("Loading RAG index")

            index, data = self.index_manager.load()

            self.store = FaissStore(index.d)
            self.store.index = index

            # ✅ FIX: assign to data (not metadata)
            self.store.data = data

            self.retriever = Retriever(self.store, self.embedder)

            logger.info("Index loaded successfully")

        except Exception:
            logger.exception("Failed to load index")
            raise RuntimeError("RAG load failed")

    # ---------------------------
    # QUERY PHASE
    # ---------------------------
    def query(self, query: str, top_k: int = 3) -> Dict:
        """
        Query pipeline
        """

        try:
            if not self.retriever:
                raise ValueError("Index not loaded")

            logger.info(f"Processing query: {query}")

            results = self.retriever.retrieve(query, top_k)
            context = self.retriever.build_context(results)

            return {
                "query": query,
                "results": results,
                "context": context
            }

        except Exception:
            logger.exception("Query failed")
            raise RuntimeError("RAG query failed")