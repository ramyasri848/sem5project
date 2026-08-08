"""
extractor.py

Module 7: Bit Extraction

Converts CA states into binary output.
"""

from typing import List


class BitExtractor:

    VALID_METHODS = {
        "full_state",
        "center_column",
        "xor_fold",
        "column_xor",
        "majority"
    }

    def __init__(
        self,
        method: str = "full_state"
    ):

        if method not in self.VALID_METHODS:
            raise ValueError(
                f"Unknown method '{method}'. "
                f"Choose from {self.VALID_METHODS}"
            )

        self.method = method

    def extract(
        self,
        history: List[List[int]]
    ) -> List[int]:

        if not history:
            return []

        if self.method == "full_state":
            return self._full_state(history)

        if self.method == "center_column":
            return self._center_column(history)

        if self.method == "xor_fold":
            return self._xor_fold(history)

        if self.method == "column_xor":
            return self._column_xor(history)

        if self.method == "majority":
            return self._majority(history)

        raise ValueError("Invalid extraction method.")

    @staticmethod
    def _full_state(
        history: List[List[int]]
    ) -> List[int]:

        bits = []

        for row in history:
            bits.extend(row)

        return bits

    @staticmethod
    def _center_column(
        history: List[List[int]]
    ) -> List[int]:

        width = len(history[0])
        center = width // 2

        return [
            row[center]
            for row in history
        ]

    @staticmethod
    def _xor_fold(
        history: List[List[int]]
    ) -> List[int]:

        bits = []

        for row in history:

            half = len(row) // 2

            left = row[:half]
            right = row[
                half:half * 2
            ]

            folded = [
                a ^ b
                for a, b in zip(
                    left,
                    right
                )
            ]

            bits.append(
                sum(folded) % 2
            )

        return bits

    @staticmethod
    def _column_xor(
        history: List[List[int]]
    ) -> List[int]:

        bits = []

        for row in history:

            parity = 0

            for cell in row:
                parity ^= cell

            bits.append(parity)

        return bits

    @staticmethod
    def _majority(
        history: List[List[int]]
    ) -> List[int]:

        bits = []

        for row in history:

            ones = sum(row)

            bits.append(
                1
                if ones > len(row) / 2
                else 0
            )

        return bits


if __name__ == "__main__":

    from ca import UniformCA

    ca = UniformCA(
        width=63,
        rule_number=30
    )

    ca.run(100)

    extractor = BitExtractor(
        method="full_state"
    )

    bits = extractor.extract(
        ca.history[1:]
    )

    print(
        "Generated bits:",
        len(bits)
    )

    print(
        "First 100 bits:",
        "".join(
            str(bit)
            for bit in bits[:100]
        )
    )