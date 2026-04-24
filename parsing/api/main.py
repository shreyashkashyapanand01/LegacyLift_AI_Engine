from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid
import os
import logging

from parsing.utils.logger import setup_logging
from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.parser import parse_project
from parsing.utils.validator import validate_project
from parsing.utils.file_writer import save_output

# 🔧 Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="LegacyLift AI Engine", version="1.0")


@app.post("/parse")
async def parse_code(file: UploadFile = File(...)):
    """
    Upload ZIP → Parse → Return structured JSON
    """

    job_id = str(uuid.uuid4())

    try:
        logger.info(f"New request received | job_id={job_id}")

        # 🔥 Step 1: Save uploaded file temporarily
        temp_zip_path = f"workspace/{job_id}_temp.zip"

        with open(temp_zip_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # 🔥 Step 2: Move into structured workspace
        saved_zip = save_input_zip(temp_zip_path, job_id)

        # Remove temp file
        os.remove(temp_zip_path)

        # 🔥 Step 3: Extract
        root_path = extract_zip(saved_zip, job_id)

        # 🔥 Step 4: Validate
        validate_project(root_path)

        # 🔥 Step 5: Scan
        files = scan_project(root_path)

        if not files:
            raise HTTPException(status_code=400, detail="No supported files found")

        # 🔥 Step 6: Parse
        result = parse_project(root_path, files)

        # 🔥 Step 7: Save output
        save_output(result, root_path)

        logger.info(f"Job completed successfully | job_id={job_id}")

        return {
            "job_id": job_id,
            "result": result
        }

    except HTTPException as e:
        logger.warning(f"Client error | job_id={job_id} | {e.detail}")
        raise e

    except Exception as e:
        logger.exception(f"Internal error | job_id={job_id}")
        raise HTTPException(status_code=500, detail="Internal server error")