import os


def validate_project(root_path: str):
    if not os.path.exists(root_path):
        raise ValueError("Project path does not exist")

    if not os.listdir(root_path):
        raise ValueError("Project directory is empty")