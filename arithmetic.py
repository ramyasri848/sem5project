"""
arithmetic.py

Module 1: Arithmetic Grammar Engine

Generates a deterministic sequence of bounded arithmetic values
from a seed.

Pipeline:
Seed -> Arithmetic Grammar -> Arithmetic Value
"""

import random
from typing import Callable, Dict, List


class ArithmeticState:
    """Stores the current arithmetic value and its history."""

    def __init__(self, seed: int):
        self.value = seed
        self.history: List[int] = [seed]

    def update(self, new_value: int) -> None:
        self.value = new_value
        self.history.append(new_value)

    def __repr__(self) -> str:
        return f"ArithmeticState(value={self.value}, steps={len(self.history)})"


class OperatorLibrary:
    """Arithmetic operators used by the grammar."""

    @staticmethod
    def add(a: int, b: int) -> int:
        return a + b

    @staticmethod
    def sub(a: int, b: int) -> int:
        return a - b

    @staticmethod
    def mul(a: int, b: int) -> int:
        return a * b

    @staticmethod
    def xor(a: int, b: int) -> int:
        return a ^ b

    @staticmethod
    def mod(a: int, b: int) -> int:
        return a % b if b != 0 else a

    @staticmethod
    def shift_left(a: int, b: int) -> int:
        return a << (b % 8)

    @staticmethod
    def shift_right(a: int, b: int) -> int:
        return a >> (b % 8)

    def all_operators(self) -> Dict[str, Callable[[int, int], int]]:
        return {
            "add": self.add,
            "sub": self.sub,
            "mul": self.mul,
            "xor": self.xor,
            "mod": self.mod,
            "shl": self.shift_left,
            "shr": self.shift_right,
        }


class ExpressionEvaluator:
    """Evaluates arithmetic operations while enforcing a modulus."""

    def __init__(self, operators: OperatorLibrary, modulus: int = 2 ** 32):
        self.operators = operators.all_operators()
        self.modulus = modulus

    def evaluate(self, value: int, operand: int, op_name: str) -> int:
        op = self.operators[op_name]

        result = op(value, operand)

        # Immediately reduce the result.
        # This prevents numbers from becoming astronomically large.
        return result % self.modulus


class ArithmeticGrammar:
    """
    Deterministic arithmetic generator.

    The same seed always produces the same sequence.
    """

    def __init__(self, seed: int, modulus: int = 2 ** 32):
        self.modulus = modulus

        self.rng = random.Random(seed)

        self.operators = OperatorLibrary()

        self.evaluator = ExpressionEvaluator(
            self.operators,
            modulus
        )

        self.state = ArithmeticState(seed % modulus)

        self.op_names = list(
            self.operators.all_operators().keys()
        )

    def step(self) -> int:
        """Generate one arithmetic value."""

        op_name = self.rng.choice(self.op_names)

        operand = self.rng.randint(
            1,
            self.modulus - 1
        )

        new_value = self.evaluator.evaluate(
            self.state.value,
            operand,
            op_name
        )

        self.state.update(new_value)

        return new_value

    def generate(self, n: int) -> List[int]:
        """Generate n arithmetic values."""

        if n <= 0:
            raise ValueError(
                "Number of values must be greater than zero."
            )

        return [
            self.step()
            for _ in range(n)
        ]


if __name__ == "__main__":

    grammar = ArithmeticGrammar(seed=12345)

    values = grammar.generate(10)

    print("=" * 60)
    print("Arithmetic Grammar Engine")
    print("=" * 60)

    for i, value in enumerate(values, 1):
        print(f"Step {i:2}: {value}")