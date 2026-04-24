from parsing.utils.logger import setup_logging
setup_logging()

import logging
import uuid

from parsing.core.zip_handler import extract_zip, save_input_zip, cleanup_workspace
from parsing.core.scanner import scan_project
from parsing.core.parser import parse_project
from parsing.utils.file_writer import save_output
from parsing.utils.validator import validate_project

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    logger.info(f"Starting job: {job_id}")

    # Step 1: Save + Extract
    saved_zip = save_input_zip(zip_path, job_id)
    root_path = extract_zip(saved_zip, job_id)

    # Step 2: Validate
    validate_project(root_path)

    # Step 3: Scan
    files = scan_project(root_path)

    if not files:
        raise ValueError("No supported files found")

    # Step 4: Parse
    result = parse_project(root_path, files)

    # Step 5: Save output
    save_output(result, root_path)

    print("\n=== FINAL OUTPUT ===\n")
    print(result)

    logger.info("Pipeline completed successfully")

except Exception as e:
    logger.exception("Pipeline failed")

finally:
    # 🔥 OPTIONAL: comment this during debugging
    # cleanup_workspace(job_id)
    pass