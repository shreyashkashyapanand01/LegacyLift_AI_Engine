def detect_language(file_path):
    if file_path.endswith(".py"):
        return "python"
    elif file_path.endswith(".java"):
        return "java"
    return "unknown"