import os


def normalize_path(path: str) -> str:
    """
    Converts Windows paths to Unix-style
    """
    return path.replace("\\", "/")


def get_relative_path(full_path: str, root_path: str) -> str:
    """
    Returns normalized relative path
    """
    relative = os.path.relpath(full_path, root_path)
    return normalize_path(relative)