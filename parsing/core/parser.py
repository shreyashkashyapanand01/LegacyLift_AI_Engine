from parsing.core.orchestrator import run_pipeline


def parse_project(root_path, files):
    return run_pipeline(root_path, files)