"""
statistics.py

Module 9: Statistical Evaluation
"""

import math
from typing import Dict, List


class StatisticalEvaluator:

    def validate_bits(
        self,
        bits: List[int]
    ) -> None:

        if not bits:
            raise ValueError(
                "Bit sequence cannot be empty."
            )

        if any(
            bit not in (0, 1)
            for bit in bits
        ):
            raise ValueError(
                "Bit sequence must contain only 0 and 1."
            )

    def monobit_test(
        self,
        bits: List[int]
    ) -> Dict:

        self.validate_bits(bits)

        n = len(bits)

        ones = sum(bits)
        zeros = n - ones

        proportion = ones / n

        total = (
            2 * ones - n
        )

        statistic = (
            abs(total)
            / math.sqrt(n)
        )

        return {
            "ones": ones,
            "zeros": zeros,
            "proportion_ones": proportion,
            "statistic": statistic
        }

    def runs_test(
        self,
        bits: List[int]
    ) -> Dict:

        self.validate_bits(bits)

        n = len(bits)

        ones = sum(bits)

        proportion = ones / n

        if proportion in (0, 1):

            return {
                "runs": 1,
                "proportion_ones": proportion,
                "expected_runs": 1,
                "statistic": float("inf"),
                "valid": False
            }

        runs = 1

        for i in range(1, n):

            if bits[i] != bits[i - 1]:
                runs += 1

        expected = (
            2
            * n
            * proportion
            * (1 - proportion)
        ) + 1

        variance = (
            2
            * n
            * proportion
            * (1 - proportion)
            * (
                2
                * n
                * proportion
                * (1 - proportion)
                - 1
            )
            / (n - 1)
        )

        statistic = (
            (runs - expected)
            / math.sqrt(variance)
        )

        return {
            "runs": runs,
            "proportion_ones": proportion,
            "expected_runs": expected,
            "statistic": statistic,
            "valid": True
        }

    def entropy(
        self,
        bits: List[int]
    ) -> float:

        self.validate_bits(bits)

        n = len(bits)

        zeros = bits.count(0)
        ones = bits.count(1)

        entropy = 0.0

        for count in (
            zeros,
            ones
        ):

            if count == 0:
                continue

            probability = count / n

            entropy -= (
                probability
                * math.log2(probability)
            )

        return entropy

    def autocorrelation(
        self,
        bits: List[int],
        lag: int = 1
    ) -> float:

        self.validate_bits(bits)

        if lag <= 0:
            raise ValueError(
                "Lag must be greater than zero."
            )

        if lag >= len(bits):
            raise ValueError(
                "Lag must be smaller than sequence length."
            )

        x = [
            1 if bit == 1 else -1
            for bit in bits
        ]

        n = len(x)

        mean = sum(x) / n

        numerator = sum(
            (x[i] - mean)
            * (x[i + lag] - mean)
            for i in range(n - lag)
        )

        denominator = sum(
            (value - mean) ** 2
            for value in x
        )

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def evaluate(
        self,
        bits: List[int]
    ) -> Dict:

        self.validate_bits(bits)

        return {
            "length": len(bits),

            "monobit":
                self.monobit_test(bits),

            "runs":
                self.runs_test(bits),

            "entropy":
                self.entropy(bits),

            "autocorrelation":
                self.autocorrelation(bits)
        }


def summary_report(
    bits: List[int]
) -> Dict:

    evaluator = StatisticalEvaluator()

    return evaluator.evaluate(bits)


def monobit_frequency(
    bits: List[int]
) -> Dict:

    evaluator = StatisticalEvaluator()

    return evaluator.monobit_test(bits)


def runs_test(
    bits: List[int]
) -> Dict:

    evaluator = StatisticalEvaluator()

    return evaluator.runs_test(bits)


if __name__ == "__main__":

    import random

    bits = [
        random.randint(0, 1)
        for _ in range(10000)
    ]

    evaluator = StatisticalEvaluator()

    results = evaluator.evaluate(bits)

    print(results)