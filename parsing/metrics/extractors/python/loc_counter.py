from parsing.metrics.extractors.base_analyzer import BaseAnalyzer


class PythonLOC:

    @staticmethod
    def analyze(code: str):
        lines = code.split("\n")

        total_lines = 0
        effective_lines = 0
        comment_lines = 0

        for line in lines:
            stripped = line.strip()

            # skip blank lines
            if not stripped:
                continue

            total_lines += 1

            # full-line comment
            if stripped.startswith("#"):
                comment_lines += 1
                continue

            # inline comment
            if "#" in stripped:
                code_part = stripped.split("#")[0].strip()
            else:
                code_part = stripped

            if code_part:
                effective_lines += 1

        return {
            "total_lines": total_lines,
            "effective_lines": effective_lines,
            "comment_lines": comment_lines
        }