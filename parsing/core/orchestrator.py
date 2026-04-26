# import os
# import logging
# from typing import List, Dict

# from parsing.analyzers.dependency_mapper import map_dependencies
# from parsing.analyzers.ast_parser import (
#     parse_python_file,
#     parse_java_file
# )

# from parsing.models.schema import build_project_schema

# logger = logging.getLogger(__name__)


# def run_pipeline(root_path: str, files: List[Dict]) -> Dict:
#     """
#     Main orchestration pipeline:
#     Scan → Parse → Dependencies → Aggregate
#     """

#     logger.info("Starting orchestration pipeline")

#     all_functions = []
#     file_metadata = []

#     try:
#         for file in files:
#             relative_path = file["path"]
#             language = file["language"]

#             full_path = os.path.join(root_path, relative_path)

#             logger.debug(f"Processing file: {relative_path} ({language})")

#             # 🔁 Route to correct parser
#             if language == "python":
#                 functions = parse_python_file(full_path, root_path)

#             elif language == "java":
#                 functions = parse_java_file(full_path, root_path)

#             else:
#                 logger.warning(f"Unsupported language: {language}")
#                 continue

#             # 🔥 Aggregate
#             all_functions.extend(functions)

#             file_metadata.append({
#                 "path": relative_path,
#                 "language": language
#             })

#         project_name = os.path.basename(root_path)

#         dependencies = map_dependencies(root_path, files)

#         # result = {
#         #     "project": project_name,
#         #     "files": file_metadata,
#         #     "functions": all_functions,
#         #     "dependencies": dependencies
#         # }
#         result = build_project_schema(
#             project=project_name,
#             files=file_metadata,
#             functions=all_functions,
#             dependencies=dependencies
#         )

#         logger.info(
#             f"Pipeline completed: {len(file_metadata)} files, "
#             f"{len(all_functions)} functions, "
#             f"{len(dependencies)} dependencies"
#         )

#         return result

#     except Exception:
#         logger.exception("Pipeline failed")
#         raise RuntimeError("Orchestration pipeline failed")


import os
import logging
from typing import List, Dict

from parsing.analyzers.dependency_mapper import map_dependencies
from parsing.analyzers.ast_parser import (
    parse_python_file,
    parse_java_file
)

from parsing.models.schema import build_project_schema

# 🔥 NEW: schema import
from parsing.shared.models.parsing_schema import ParsingOutput

logger = logging.getLogger(__name__)


# ---------------------------
# 🔥 NORMALIZER (VERY IMPORTANT)
# ---------------------------
def normalize_output(result: Dict) -> Dict:
    """
    Convert parser output → schema-compatible format
    """

    # 🔹 Fix functions
    for func in result.get("functions", []):
        func["function"] = func.pop("name", "")
        func["code"] = func.get("code", "")  

    # 🔹 Fix dependencies
    for dep in result.get("dependencies", []):
        dep["source"] = dep.pop("from", "")
        dep["target"] = dep.pop("to", "")

    return result


# ---------------------------
# 🚀 MAIN PIPELINE
# ---------------------------
def run_pipeline(root_path: str, files: List[Dict]) -> Dict:
    """
    Scan -> Parse -> Dependencies -> Normalize -> Validate
    """

    logger.info("Starting orchestration pipeline")

    all_functions = []
    file_metadata = []

    try:
        for file in files:
            relative_path = file["path"]
            language = file["language"]

            full_path = os.path.join(root_path, relative_path)

            logger.debug(f"Processing file: {relative_path} ({language})")

            # 🔁 Route to correct parser
            if language == "python":
                functions = parse_python_file(full_path, root_path)

            elif language == "java":
                functions = parse_java_file(full_path, root_path)

            else:
                logger.warning(f"Unsupported language: {language}")
                continue

            # 🔥 Aggregate
            all_functions.extend(functions)

            file_metadata.append({
                "path": relative_path,
                "language": language
            })

        project_name = os.path.basename(root_path)

        dependencies = map_dependencies(root_path, files)

        # 🔹 Build raw result (old format)
        result = build_project_schema(
            project=project_name,
            files=file_metadata,
            functions=all_functions,
            dependencies=dependencies
        )

        # 🔥 STEP 1: Normalize
        result = normalize_output(result)

        # 🔥 STEP 2: Validate with schema
        validated = ParsingOutput(**result)

        logger.info(
            f"Pipeline completed: {len(file_metadata)} files, "
            f"{len(all_functions)} functions, "
            f"{len(dependencies)} dependencies"
        )

        # 🔥 STEP 3: Return clean dict
        return validated.model_dump()

    except Exception:
        logger.exception("Pipeline failed")
        raise RuntimeError("Orchestration pipeline failed")