from parsing.utils.logger import setup_logging
setup_logging()

import logging
import uuid

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.orchestrator import run_pipeline
from parsing.rag.preprocessing.document_builder import build_documents
from parsing.rag.chunking.code_chunker import chunk_documents

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    # Module 1
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    files = scan_project(root_path)
    parsed_output = run_pipeline(root_path, files)

    # Module 2 step 1
    documents = build_documents(parsed_output, root_path)

    # 🔥 Chunking
    chunks = chunk_documents(documents, root_path)

    print("\n=== CHUNKS ===\n")

    for chunk in chunks:
        print(chunk["metadata"])
        print(chunk["text"])
        print("=" * 50)

except Exception:
    logger.exception("Test failed")