from parsing.utils.logger import setup_logging
setup_logging()

import logging
import uuid

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.rag.pipeline.rag_pipeline import RAGPipeline

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    # Step 1: extract project
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    # Step 2: RAG pipeline
    pipeline = RAGPipeline(index_dir=f"workspace/{job_id}/index")

    # 🔥 Build index
    pipeline.build_index(root_path)

    # 🔥 Load index
    pipeline.load_index()

    # 🔍 Query
    response = pipeline.query("function to add numbers", top_k=2)

    print("\n=== RETRIEVED RESULTS ===\n")

    for r in response["results"]:
        print(r["score"])
        print(r["function"], "->", r["file"])
        print(r["code"])
        print("-" * 50)

    print("\n=== FINAL CONTEXT ===\n")
    print(response["context"])

except Exception:
    logger.exception("Test failed")