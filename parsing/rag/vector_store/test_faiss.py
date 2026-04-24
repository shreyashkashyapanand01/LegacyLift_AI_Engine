from parsing.utils.logger import setup_logging
setup_logging()

import logging
import uuid

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.orchestrator import run_pipeline

from parsing.rag.preprocessing.document_builder import build_documents
from parsing.rag.chunking.code_chunker import chunk_documents
from parsing.rag.embedding.embedder import Embedder

from parsing.rag.vector_store.faiss_store import FaissStore

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    # Module 1
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    files = scan_project(root_path)
    parsed_output = run_pipeline(root_path, files)

    # Module 2
    docs = build_documents(parsed_output, root_path)
    chunks = chunk_documents(docs, root_path)

    texts = [c["text"] for c in chunks]
    metadata = chunks

    # 🔥 Embedding
    embedder = Embedder()
    vectors = embedder.embed_documents(texts)

    # 🔥 FAISS
    dim = vectors.shape[1]
    store = FaissStore(dim)

    store.add(vectors, metadata)

    # 🔍 Test search
    query = "function to add two numbers"
    q_vec = embedder.embed_query(query)

    results = store.search(q_vec, top_k=2)

    print("\n=== SEARCH RESULTS ===\n")
    for r in results:
        print(r["score"])
        print(r["metadata"])
        print("-" * 50)

except Exception:
    logger.exception("Test failed")