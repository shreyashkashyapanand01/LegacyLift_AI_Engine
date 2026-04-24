import os
import logging

from parsing.utils.file_utils import write_json

logger = logging.getLogger(__name__)


def save_output(result: dict, root_path: str):
    try:
        # workspace_path = os.path.dirname(root_path)
        # output_path = os.path.join(workspace_path, "output.json")
        
        workspace_path = os.path.dirname(os.path.dirname(root_path))
        output_path = os.path.join(workspace_path, "output.json")

        write_json(output_path, result)

        logger.info(f"Output saved at: {output_path}")

    except Exception:
        logger.exception("Failed to save output")
        raise RuntimeError("Output saving failed")