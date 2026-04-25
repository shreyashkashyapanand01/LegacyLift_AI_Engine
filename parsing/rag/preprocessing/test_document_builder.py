from parsing.utils.logger import setup_logging
setup_logging()

import logging
import uuid

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.orchestrator import run_pipeline
from parsing.rag.preprocessing.document_builder import build_documents

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    # Step 1: Module 1 pipeline
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    files = scan_project(root_path)
    parsed_output = run_pipeline(root_path, files)

    # Step 2: Document builder
    documents = build_documents(parsed_output, root_path)

    print("\n=== DOCUMENTS ===\n")

    for doc in documents:
        print(doc["metadata"])
        print(doc["text"])
        print("-" * 50)

except Exception:
    logger.exception("Test failed")