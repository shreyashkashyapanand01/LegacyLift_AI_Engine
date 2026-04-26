from parsing.rag.refactor_engine.pipeline.refactor_pipeline import RefactorPipeline

original = """public int sum(int a,int b){return a+b;}"""

refactored = """public int sum(int a, int b) {
    return Math.addExact(a, b);
}"""

result = RefactorPipeline.run(original, refactored)

import json
print(json.dumps(result, indent=2))