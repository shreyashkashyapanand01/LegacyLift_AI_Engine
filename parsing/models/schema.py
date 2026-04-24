from typing import List, Dict


def build_project_schema(
    project: str,
    files: List[Dict],
    functions: List[Dict],
    dependencies: List[Dict]
) -> Dict:
    """
    Standardized schema builder for project output
    """

    return {
        "project": project,
        "files": files,
        "functions": functions,
        "dependencies": dependencies
    }