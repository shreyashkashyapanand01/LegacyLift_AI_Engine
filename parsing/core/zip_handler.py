import zipfile
import os
import logging

import shutil

logger = logging.getLogger(__name__)

# 🔥 Base workspace directory
WORKSPACE_DIR = "workspace"


def extract_zip(zip_path: str, job_id: str) -> str:
    """
    Extract zip into structured workspace

    Returns:
        extracted folder path
    """

    if not zipfile.is_zipfile(zip_path):
        logger.error(f"Invalid zip file: {zip_path}")
        raise ValueError("Invalid zip file")

    # 🔥 Create workspace paths
    job_dir = os.path.join(WORKSPACE_DIR, job_id)
    extract_dir = os.path.join(job_dir, "extracted")

    os.makedirs(extract_dir, exist_ok=True)

    logger.info(f"Extracting zip into workspace: {extract_dir}")

    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        logger.info("Extraction completed")

        # 🔥 Detect root folder
        root_path = _get_project_root(extract_dir)

        logger.info(f"Detected project root: {root_path}")

        return root_path

    except Exception as e:
        logger.exception("Zip extraction failed")
        raise RuntimeError("Failed to extract zip") from e


def save_input_zip(original_zip_path: str, job_id: str) -> str:
    """
    Save original zip into workspace/input.zip
    """

    job_dir = os.path.join(WORKSPACE_DIR, job_id)
    os.makedirs(job_dir, exist_ok=True)

    dest_path = os.path.join(job_dir, "input.zip")

    with open(original_zip_path, "rb") as src, open(dest_path, "wb") as dst:
        dst.write(src.read())

    logger.info(f"Saved input zip to: {dest_path}")

    return dest_path


def _get_project_root(base_path: str) -> str:
    """
    Detects if zip has single root folder
    """

    try:
        items = os.listdir(base_path)
        items = [i for i in items if not i.startswith(".") and not i.startswith("__")]

        if len(items) == 1:
            candidate = os.path.join(base_path, items[0])
            if os.path.isdir(candidate):
                return candidate

        return base_path

    except Exception:
        logger.warning("Could not determine project root")
        return base_path
    


def cleanup_workspace(job_id: str):
    base_path = f"workspace/{job_id}"

    try:
        if os.path.exists(base_path):
            shutil.rmtree(base_path)
    except Exception:
        logger.warning(f"Cleanup failed for job: {job_id}")