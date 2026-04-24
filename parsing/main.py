from fastapi import FastAPI
from parsing.parser import parse_project

app = FastAPI()

@app.post("/parse")
def parse_code(request: dict):
    path = request.get("path")
    result = parse_project(path)
    return result