import uuid
import os
import logging

from fastapi import UploadFile, HTTPException

from parsing.core.zip_handler import save_input_zip, extract_zip
from parsing.core.scanner import scan_project
from parsing.core.parser import parse_project
from parsing.utils.validator import validate_project
from parsing.utils.file_writer import save_output

logger = logging.getLogger(__name__)


class ParseService:

    async def parse(self, file: UploadFile):
        job_id = str(uuid.uuid4())

        try:
            logger.info(f"New parse request | job_id={job_id}")

            temp_zip_path = f"workspace/{job_id}_temp.zip"

            with open(temp_zip_path, "wb") as f:
                content = await file.read()
                f.write(content)

            saved_zip = save_input_zip(temp_zip_path, job_id)
            os.remove(temp_zip_path)

            root_path = extract_zip(saved_zip, job_id)

            validate_project(root_path)

            files = scan_project(root_path)

            if not files:
                raise HTTPException(status_code=400, detail="No supported files found")

            result = parse_project(root_path, files)

            save_output(result, root_path)

            logger.info(f"Parse completed | job_id={job_id}")

            return {
                "job_id": job_id,
                "result": result
            }

        except HTTPException as e:
            logger.warning(f"Client error | job_id={job_id} | {e.detail}")
            raise e

        except Exception:
            logger.exception(f"Internal error | job_id={job_id}")
            raise HTTPException(status_code=500, detail="Internal server error")