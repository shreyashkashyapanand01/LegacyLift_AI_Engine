from parsing.file_scanner import scan_files
from parsing.language_detector import detect_language
from parsing.ast_parser import parse_file

def parse_project(path):
    files = scan_files(path)

    parsed_files = []
    functions = []
    dependencies = []

    for file in files:
        lang = detect_language(file)

        parsed = parse_file(file, lang)

        parsed_files.append({
            "name": file,
            "language": lang
        })

        functions.extend(parsed.get("functions", []))
        dependencies.extend(parsed.get("dependencies", []))

    return {
        "files": parsed_files,
        "functions": functions,
        "dependencies": dependencies
    }