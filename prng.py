"""
prng.py

Module 8: KnuthCA_PRNG

Complete pipeline:

Seed
  ↓
Arithmetic Grammar
  ↓
Feature Extraction
  ↓
Adaptive Rule Scheduler
  ↓
Non-Uniform Cellular Automaton
  ↓
Bit Extraction
"""

from typing import List

from arithmetic import ArithmeticGrammar
from arithmetic_features import ArithmeticFeatureExtractor
from scheduler import AdaptiveRuleScheduler
from ca import NonUniformCA
from extractor import BitExtractor


class KnuthCA_PRNG:

    def __init__(
        self,
        seed: int,
        ca_width: int = 101,
        extraction_method: str = "full_state"
    ):

        if ca_width <= 0:
            raise ValueError(
                "CA width must be greater than zero."
            )

        self.seed = seed
        self.ca_width = ca_width

        self.grammar = ArithmeticGrammar(
            seed=seed
        )

        self.feature_extractor = (
            ArithmeticFeatureExtractor()
        )

        self.scheduler = (
            AdaptiveRuleScheduler()
        )

        self.ca = NonUniformCA(
            width=ca_width
        )

        self.bit_extractor = BitExtractor(
            method=extraction_method
        )

        self.arithmetic_values = []
        self.feature_vectors = []
        self.rule_sequence = []

    def generate(
        self,
        iterations: int,
        store_history: bool = False
    ) -> List[int]:

        if iterations <= 0:
            raise ValueError(
                "Iterations must be greater than zero."
            )

        generated_bits = []

        # Generate arithmetic values.
        self.arithmetic_values = (
            self.grammar.generate(iterations)
        )

        # Extract features.
        self.feature_vectors = [
            self.feature_extractor.extract_features(
                value
            )
            for value in self.arithmetic_values
        ]

        # Select CA rules.
        self.rule_sequence = (
            self.scheduler.select_rule_sequence(
                self.feature_vectors
            )
        )

        # Reset CA history.
        self.ca.history = [
            self.ca.state.copy()
        ]

        self.ca.rule_history = []

        # Generate CA states.
        for rule in self.rule_sequence:

            state = self.ca.step(
                rule,
                store_history=store_history
            )

            # Full CA state becomes output.
            generated_bits.extend(state)

        return generated_bits

    def generate_bits(
        self,
        num_bits: int
    ) -> List[int]:

        if num_bits <= 0:
            raise ValueError(
                "Number of bits must be greater than zero."
            )

        # Number of CA generations needed.
        iterations = (
            num_bits + self.ca_width - 1
        ) // self.ca_width

        bits = self.generate(
            iterations,
            store_history=False
        )

        return bits[:num_bits]

    def generate_bytes(
        self,
        num_bytes: int
    ) -> bytes:

        if num_bytes <= 0:
            raise ValueError(
                "Number of bytes must be greater than zero."
            )

        bits = self.generate_bits(
            num_bytes * 8
        )

        output = bytearray()

        for i in range(
            0,
            len(bits),
            8
        ):

            value = 0

            for bit in bits[i:i + 8]:

                value = (
                    value << 1
                ) | bit

            output.append(value)

        return bytes(output)

    def generate_int(
        self,
        bits_needed: int = 32
    ) -> int:

        bits = self.generate_bits(
            bits_needed
        )

        value = 0

        for bit in bits:

            value = (
                value << 1
            ) | bit

        return value


if __name__ == "__main__":

    print("=" * 60)
    print("KnuthCA_PRNG Pipeline Test")
    print("=" * 60)

    generator = KnuthCA_PRNG(
        seed=12345,
        ca_width=101
    )

    bits = generator.generate(
        iterations=100
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

    print(
        "Rules used:",
        generator.rule_sequence[:20]
    )

    random_bytes = generator.generate_bytes(16)

    print(
        "Random bytes:",
        random_bytes.hex()
    )