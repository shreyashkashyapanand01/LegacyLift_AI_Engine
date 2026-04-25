import json
import logging

logger = logging.getLogger(__name__)


def clean_response(response: str):
    try:
        # 🔥 Try direct JSON parse
        return json.loads(response)

    except Exception:
        logger.warning("Raw LLM response not valid JSON, attempting cleanup")

        try:
            # 🔥 Extract JSON block manually
            start = response.find("{")
            end = response.rfind("}") + 1

            json_str = response[start:end]

            return json.loads(json_str)

        except Exception:
            logger.exception("Failed to parse LLM response")

            # fallback (never crash API)
            return {
                "explanation": response,
                "code_reference": "",
                "examples": []
            }