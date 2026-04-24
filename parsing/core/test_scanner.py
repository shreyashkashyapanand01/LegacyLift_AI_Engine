from parsing.utils.logger import setup_logging
setup_logging()

import uuid
import logging
from parsing.core.scanner import scan_project
from parsing.core.zip_handler import extract_zip, save_input_zip

logger = logging.getLogger(__name__)

zip_path = "C:/Users/KIIT/Downloads/test-project.zip"
job_id = str(uuid.uuid4())

try:
    logger.info(f"Starting job: {job_id}")

    # 🔥 Step 1: Save zip to workspace
    saved_zip = save_input_zip(zip_path, job_id)

    # 🔥 Step 2: Extract
    folder_path = extract_zip(saved_zip, job_id)

    # 🔥 Step 3: Scan
    result = scan_project(folder_path)

    for file in result:
        print(file)

    logger.info("Pipeline completed successfully")

except Exception:
    logger.exception("Pipeline failed")