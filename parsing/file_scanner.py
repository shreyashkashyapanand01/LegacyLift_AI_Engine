import os

def scan_files(root_path):
    code_files = []

    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".py") or file.endswith(".java"):
                code_files.append(os.path.join(root, file))

    return code_files