import re


class BaseAnalyzer:

    @staticmethod
    def normalize_code(code: str) -> str:
        """
        Clean and normalize code input
        """
        if not code:
            return ""

        # remove leading/trailing spaces
        code = code.strip()

        # normalize line endings
        code = code.replace("\r\n", "\n")

        return code

    # ---------------------------
    # 📏 SPLIT LINES
    # ---------------------------
    @staticmethod
    def get_lines(code: str):
        code = BaseAnalyzer.normalize_code(code)
        return [line for line in code.split("\n") if line.strip()]

    # ---------------------------
    # 🔤 TOKEN EXTRACTION
    # ---------------------------
    @staticmethod
    def tokenize(code: str):
        """
        Basic tokenizer for metrics
        """
        return re.findall(r"[A-Za-z_]\w*|\d+|[^\sA-Za-z_]", code)

    # ---------------------------
    # 🧠 OPERATOR / OPERAND SPLIT
    # ---------------------------
    @staticmethod
    # def get_operators_operands(tokens):
    #     operators = []
    #     operands = []

    #     for token in tokens:
    #         if re.match(r"[+\-*/=<>!&|%^]+", token):
    #             operators.append(token)
    #         elif re.match(r"[A-Za-z_]\w+|\d+", token):
    #             operands.append(token)

    #     return operators, operands
    
    
    
    @staticmethod
    def get_operators_operands(tokens):
        operators = []
        operands = []

        # Define operator set
        operator_set = {
            "+", "-", "*", "/", "%", "=",
            "==", "!=", ">", "<", ">=", "<=",
            "&&", "||", "!", "&", "|", "^",
            "(", ")", "{", "}", "[", "]",
            ",", ";", ".", ":", "?"
        }

        # Keywords treated as operators
        keyword_operators = {
            "return", "if", "else", "for", "while",
            "switch", "case", "break", "continue",
            "try", "catch", "throw"
        }

        for token in tokens:

            if token in operator_set or token in keyword_operators:
                operators.append(token)

            elif token.isidentifier() or token.isdigit():
                operands.append(token)

        return operators, operands

    # ---------------------------
    # 🔍 DECISION KEYWORDS (GENERIC)
    # ---------------------------
    @staticmethod
    def count_decision_points(code: str, keywords: list):
        count = 0
        for kw in keywords:
            count += len(re.findall(rf"\b{kw}\b", code))
        return count