import os
import uuid
import logging

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.orchestrator import run_pipeline

from parsing.rag.preprocessing.document_builder import build_documents
from parsing.rag.chunking.code_chunker import chunk_documents
from parsing.rag.embedding.embedder import Embedder
from parsing.rag.vector_store.faiss_store import FaissStore
from parsing.rag.vector_store.index_manager import IndexManager
from parsing.rag.retrieval.retriever import Retriever

logger = logging.getLogger(__name__)


class RagService:

    def __init__(self):
        self.embedder = Embedder()

    # ----------------------------------
    # 🔥 INDEX PROJECT
    # ----------------------------------
    def index_project(self, zip_path: str) -> str:
        try:
            job_id = str(uuid.uuid4())

            saved_zip = save_input_zip(zip_path, job_id)
            root_path = extract_zip(saved_zip, job_id)

            files = scan_project(root_path)
            parsed_output = run_pipeline(root_path, files)

            docs = build_documents(parsed_output, root_path)
            chunks = chunk_documents(docs, root_path)

            texts = [c["text"] for c in chunks]
            vectors = self.embedder.embed_documents(texts)

            store = FaissStore(vectors.shape[1])
            store.add(vectors, chunks)

            # ✅ FIX: correct path + correct metadata
            index_path = os.path.join("workspace", job_id)
            os.makedirs(index_path, exist_ok=True)

            manager = IndexManager(index_path)
            manager.save(store.index, store.data)   # 🔥 FIXED

            logger.info(f"Indexing completed for job_id={job_id}")

            return job_id

        except Exception:
            logger.exception("Indexing failed")
            raise RuntimeError("Indexing failed")

    # ----------------------------------
    # 🔍 QUERY
    # ----------------------------------
    def query(self, job_id: str, query: str, top_k: int = 3):
        try:
            # ✅ THIS is where path should be used
            index_path = os.path.join("workspace", job_id)

            manager = IndexManager(index_path)
            index, data = manager.load()

            store = FaissStore(index.d)
            store.index = index
            store.data = data   # 🔥 FIXED

            retriever = Retriever(store, self.embedder)

            results = retriever.retrieve(query, top_k=top_k)
            context = retriever.build_context(results)

            return {
                "results": results,
                "context": context
            }

        except Exception:
            logger.exception("Query failed")
            raise RuntimeError("Query failed")