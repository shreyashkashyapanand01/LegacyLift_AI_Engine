from parsing.metrics.extractors.base_analyzer import BaseAnalyzer


class JavaLOC:

    @staticmethod
    def analyze(code: str):
        lines = code.split("\n")

        total_lines = 0
        effective_lines = 0
        comment_lines = 0

        in_block_comment = False

        for line in lines:
            stripped = line.strip()

            if not stripped:
                continue

            # ---------------------------
            # BLOCK COMMENTS
            # ---------------------------
            if stripped.startswith("/*"):
                in_block_comment = True
                comment_lines += 1
                continue

            if "*/" in stripped:
                in_block_comment = False
                comment_lines += 1
                continue

            if in_block_comment:
                comment_lines += 1
                continue

            # ---------------------------
            # SINGLE LINE COMMENT
            # ---------------------------
            if stripped.startswith("//"):
                comment_lines += 1
                continue

            # ---------------------------
            # INLINE COMMENT
            # ---------------------------
            if "//" in stripped:
                code_part = stripped.split("//")[0].strip()
            else:
                code_part = stripped

            # ---------------------------
            # IGNORE ONLY PURE STRUCTURE
            # ---------------------------
            if code_part in ["{", "}", ";"]:
                continue

            # ✅ Count valid line
            total_lines += 1

            if code_part:
                effective_lines += 1

        return {
            "total_lines": total_lines,
            "effective_lines": effective_lines,
            "comment_lines": comment_lines
        }