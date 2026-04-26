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

from parsing.rag.agents.agent_service import AgentService
from parsing.rag.refactor_engine.pipeline.refactor_pipeline import RefactorPipeline

logger = logging.getLogger(__name__)


class RagService:

    def __init__(self):
        self.embedder = Embedder()
        self.agent_service = AgentService()

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

            index_path = os.path.join("workspace", job_id)
            os.makedirs(index_path, exist_ok=True)

            manager = IndexManager(index_path)
            manager.save(store.index, store.data)

            logger.info(f"Indexing completed for job_id={job_id}")

            return job_id

        except Exception:
            logger.exception("Indexing failed")
            raise RuntimeError("Indexing failed")

    # ----------------------------------
    # 🔍 QUERY (FINAL)
    # ----------------------------------
    def query(self, job_id: str, query: str, top_k: int = 3):
        try:
            # 🔹 Load index
            index_path = os.path.join("workspace", job_id)

            manager = IndexManager(index_path)
            index, data = manager.load()

            store = FaissStore(index.d)
            store.index = index
            store.data = data

            retriever = Retriever(store, self.embedder)

            # 🔹 Retrieve
            results = retriever.retrieve(query, top_k=top_k)

            if not results:
                return {
                    "results": [],
                    "context": "",
                    "analysis": None,
                    "refactor": None,
                    "refactor_engine": None,
                    "tests": None,
                    "validation": None
                }

            # ✅ ALWAYS USE TOP RESULT
            top_result = results[0]
            context = retriever.build_context([top_result])

            # 🔥 AGENT PIPELINE
            final_state = self.agent_service.run(query, context)

            # 🔥 Safety: dict → AgentState
            if isinstance(final_state, dict):
                from parsing.rag.agents.schemas.agent_schema import AgentState
                final_state = AgentState(**final_state)

            # 🔥 Extract outputs
            analysis = final_state.analysis.model_dump() if final_state.analysis else None
            refactor_raw = final_state.refactor.model_dump() if final_state.refactor else None
            tests = final_state.tests.model_dump() if final_state.tests else None
            validation = final_state.validation.model_dump() if final_state.validation else None

            # ==================================
            # 🔥 MODULE 4 (SAFE INTEGRATION)
            # ==================================
            refactor_engine_output = None

            try:
                if refactor_raw:
                    original_code = top_result["code"]
                    refactored_code = refactor_raw.get("code", "")

                    # 🔒 skip invalid / empty / multi-file outputs
                    if refactored_code.strip() and "File:" not in refactored_code:
                        refactor_engine_output = RefactorPipeline.run(
                            original_code=original_code,
                            refactored_code=refactored_code
                        )
                    else:
                        logger.warning("Skipping refactor engine (invalid or multi-file output)")

            except Exception:
                logger.exception("Refactor engine failed")
                refactor_engine_output = None

            # ==================================
            # 🔥 FINAL RESPONSE
            # ==================================
            return {
                "results": results,
                "context": context,
                "analysis": analysis,
                "refactor": refactor_raw,
                "refactor_engine": refactor_engine_output,
                "tests": tests,
                "validation": validation
            }

        except Exception:
            logger.exception("Query failed")
            raise RuntimeError("Query failed")