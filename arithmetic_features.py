"""
arithmetic_features.py

Module 2: Arithmetic Feature Extraction

Extracts mathematical properties from arithmetic values.
"""

from typing import Dict, List


class ArithmeticFeatureExtractor:
    """Extracts mathematical features from arithmetic values."""

    def __init__(self):
        pass

    def digit_sum(self, value: int) -> int:
        """Return the sum of decimal digits."""

        return sum(
            int(digit)
            for digit in str(abs(value))
        )

    def parity(self, value: int) -> str:
        """Return Even or Odd."""

        return "Even" if value % 2 == 0 else "Odd"

    def binary_weight(self, value: int) -> int:
        """Return the number of 1 bits."""

        return bin(abs(value)).count("1")

    def bit_transitions(self, value: int) -> int:
        """Count transitions between adjacent binary bits."""

        binary = bin(abs(value))[2:]

        if len(binary) <= 1:
            return 0

        return sum(
            binary[i] != binary[i - 1]
            for i in range(1, len(binary))
        )

    def modulo_features(self, value: int) -> Dict[str, int]:
        """Calculate useful modular features."""

        return {
            "mod2": value % 2,
            "mod3": value % 3,
            "mod5": value % 5,
            "mod7": value % 7,
            "mod11": value % 11,
        }

    def prime_factors(self, value: int) -> List[int]:
        """
        Return prime factors.

        Since arithmetic.py limits values to 32 bits,
        this function remains computationally manageable.
        """

        n = abs(value)

        if n < 2:
            return []

        factors = []

        while n % 2 == 0:
            factors.append(2)
            n //= 2

        divisor = 3

        while divisor * divisor <= n:

            while n % divisor == 0:
                factors.append(divisor)
                n //= divisor

            divisor += 2

        if n > 1:
            factors.append(n)

        return factors

    def extract_features(self, value: int) -> Dict:
        """Return the complete feature vector."""

        features = {
            "value": value,
            "digit_sum": self.digit_sum(value),
            "parity": self.parity(value),
            "binary_weight": self.binary_weight(value),
            "bit_transitions": self.bit_transitions(value),
            "prime_factors": self.prime_factors(value),
        }

        features.update(
            self.modulo_features(value)
        )

        return features


if __name__ == "__main__":

    extractor = ArithmeticFeatureExtractor()

    value = 2378

    print("=" * 60)
    print("Arithmetic Feature Extraction")
    print("=" * 60)

    print(f"\nArithmetic Value : {value}\n")

    features = extractor.extract_features(value)

    for key, val in features.items():
        print(f"{key:20}: {val}")