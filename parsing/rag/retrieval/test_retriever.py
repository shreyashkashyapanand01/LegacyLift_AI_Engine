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
from parsing.rag.retrieval.retriever import Retriever

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    # 🔹 Module 1
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    files = scan_project(root_path)
    parsed_output = run_pipeline(root_path, files)
    
     #🔥 ADD THIS BLOCK
    import json

    print("\n=== PARSED OUTPUT SAMPLE ===\n")

    print(json.dumps({
        "functions": parsed_output.get("functions", [])[:1],
        "dependencies": parsed_output.get("dependencies", [])[:1]
    }, indent=2))

    # 🔹 Module 2
    docs = build_documents(parsed_output, root_path)
    chunks = chunk_documents(docs, root_path)

    texts = [c["text"] for c in chunks]

    embedder = Embedder()
    vectors = embedder.embed_documents(texts)

    store = FaissStore(vectors.shape[1])
    store.add(vectors, chunks)

    # 🔥 Retriever
    retriever = Retriever(store, embedder)

    query = "function to add numbers"
    results = retriever.retrieve(query, top_k=2)

    context = retriever.build_context(results)

    print("\n=== RETRIEVED RESULTS ===\n")

    for r in results:
        print(r["score"])

        # ✅ NEW FORMAT (FLAT STRUCTURE)
        print(r["function"], "->", r["file"])
        print(r["code"])

        print("-" * 50)

    print("\n=== FINAL CONTEXT ===\n")
    print(context)

except Exception:
    logger.exception("Test failed")