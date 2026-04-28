import re
import logging

logger = logging.getLogger(__name__)


class TestInjector:

    # ---------------------------
    # 🚀 MAIN ENTRY
    # ---------------------------
    @staticmethod
    def parse_tests(tests: dict):
        try:
            all_tests = []

            unit_tests = tests.get("unit_tests", [])
            edge_cases = tests.get("edge_cases", [])

            for test in unit_tests + edge_cases:
                parsed = TestInjector._parse_single_test(test)

                if parsed:
                    all_tests.append(parsed)

            return all_tests

        except Exception:
            logger.exception("Test parsing failed")
            return []

    # ---------------------------
    # 🔍 SINGLE TEST PARSER
    # ---------------------------
    @staticmethod
    def _parse_single_test(test_str: str):
        test_str = test_str.strip()

        # ---------------------------
        # 🧪 RETURN TEST
        # Example:
        # multiply(2, 3) returns 6
        # ---------------------------
        match_return = re.match(
            r"(\w+)\((.*?)\)\s+returns\s+(.+)",
            test_str
        )

        if match_return:
            function = match_return.group(1)
            raw_inputs = match_return.group(2)
            expected = match_return.group(3)

            inputs = TestInjector._parse_inputs(raw_inputs)
            expected = TestInjector._parse_value(expected)

            return {
                "type": "return",
                "function": function,
                "inputs": inputs,
                "expected": expected
            }

        # ---------------------------
        # ⚠️ EXCEPTION TEST
        # Example:
        # multiply(Integer.MAX_VALUE, 2) throws ArithmeticException
        # ---------------------------
        match_exception = re.match(
            r"(\w+)\((.*?)\)\s+throws\s+(\w+)",
            test_str
        )

        if match_exception:
            function = match_exception.group(1)
            raw_inputs = match_exception.group(2)
            exception = match_exception.group(3)

            inputs = TestInjector._parse_inputs(raw_inputs)

            return {
                "type": "exception",
                "function": function,
                "inputs": inputs,
                "expected_exception": exception
            }

        logger.warning(f"Unrecognized test format: {test_str}")
        return None

    # ---------------------------
    # 🔢 INPUT PARSER
    # ---------------------------
    @staticmethod
    def _parse_inputs(input_str: str):
        inputs = []

        for val in input_str.split(","):
            val = val.strip()
            inputs.append(TestInjector._parse_value(val))

        return inputs

    # ---------------------------
    # 🔢 VALUE PARSER
    # ---------------------------
    @staticmethod
    def _parse_value(value: str):
        value = value.strip()

        # ---------------------------
        # JAVA CONSTANTS
        # ---------------------------
        if value == "Integer.MAX_VALUE":
            return 2147483647

        if value == "Integer.MIN_VALUE":
            return -2147483648

        # ---------------------------
        # NUMBERS
        # ---------------------------
        if re.match(r"^-?\d+$", value):
            return int(value)

        if re.match(r"^-?\d+\.\d+$", value):
            return float(value)

        # ---------------------------
        # STRING
        # ---------------------------
        if value.startswith('"') and value.endswith('"'):
            return value.strip('"')

        return value  # fallback