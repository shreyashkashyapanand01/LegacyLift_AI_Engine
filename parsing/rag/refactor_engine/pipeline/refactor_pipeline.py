import logging

from parsing.rag.refactor_engine.cleaner.code_cleaner import CodeCleaner
from parsing.rag.refactor_engine.utils.code_utils import CodeUtils
from parsing.rag.refactor_engine.diff.diff_generator import DiffGenerator
from parsing.rag.refactor_engine.explanation.explanation_builder import ExplanationBuilder
from parsing.rag.refactor_engine.validation.syntax_validator import SyntaxValidator

logger = logging.getLogger(__name__)


class RefactorPipeline:

    @staticmethod
    def run(original_code: str, refactored_code: str):
        try:
            # ---------------------------
            # 🧹 CLEAN
            # ---------------------------
            clean_original = CodeCleaner.clean(original_code)
            clean_refactored = CodeCleaner.clean(refactored_code)

            # ---------------------------
            # 🔍 DETECT LANGUAGE
            # ---------------------------
            language = CodeUtils.detect_language(clean_refactored or clean_original)

            # ---------------------------
            # 🎨 FORMAT
            # ---------------------------
            formatted_original, _ = CodeUtils.format_code(clean_original, language)
            formatted_refactored, formatting_applied = CodeUtils.format_code(clean_refactored, language)

            # ---------------------------
            # 🔒 SYNTAX VALIDATION (🔥 NEW)
            # ---------------------------
            validation = SyntaxValidator.validate(formatted_refactored, language)

            # ---------------------------
            # 🔍 DIFF
            # ---------------------------
            diff = DiffGenerator.generate(formatted_original, formatted_refactored)

            # ---------------------------
            # 🧠 EXPLANATION
            # ---------------------------
            explanations = ExplanationBuilder.build(diff)

            # ---------------------------
            # 📤 FINAL OUTPUT
            # ---------------------------
            return {
                "language": language,
                "formatting_applied": formatting_applied,
                "original_code": formatted_original,
                "refactored_code": formatted_refactored,
                "diff": diff,
                "explanations": explanations,
                "validation": validation   # 🔥 NEW
            }

        except Exception:
            logger.exception("Refactor pipeline failed")

            return {
                "language": "unknown",
                "formatting_applied": False,
                "original_code": original_code,
                "refactored_code": refactored_code,
                "diff": {},
                "explanations": [],
                "validation": {
                    "is_valid": False,
                    "errors": ["Pipeline failure"]
                }
            }