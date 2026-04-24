import ast
import javalang

def parse_file(file_path, language):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()

        if language == "python":
            tree = ast.parse(code)
            functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]

            return {
                "functions": [{"name": fn, "file": file_path} for fn in functions],
                "dependencies": []
            }

        elif language == "java":
            tree = javalang.parse.parse(code)
            functions = [node.name for path, node in tree if isinstance(node, javalang.tree.MethodDeclaration)]

            return {
                "functions": [{"name": fn, "file": file_path} for fn in functions],
                "dependencies": []
            }

    except Exception as e:
        return {"functions": [], "dependencies": []}