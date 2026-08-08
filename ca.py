"""
ca.py

Modules 5 & 6: Cellular Automata

Implements:
    UniformCA
    NonUniformCA
"""

from typing import List, Optional

from rule_library import RuleLibrary


class NonUniformCA:
    """
    One-dimensional binary CA.

    The rule can change at every generation.
    """

    def __init__(
        self,
        width: int,
        seed_state: Optional[List[int]] = None
    ):

        if width <= 0:
            raise ValueError(
                "CA width must be greater than zero."
            )

        self.width = width

        if seed_state is None:

            self.state = [0] * width

            self.state[
                width // 2
            ] = 1

        else:

            if len(seed_state) != width:
                raise ValueError(
                    "Seed state length must equal width."
                )

            self.state = list(seed_state)

        self.history: List[List[int]] = [
            self.state.copy()
        ]

        self.rule_history: List[int] = []

    def step(
        self,
        rule_number: int,
        store_history: bool = True
    ) -> List[int]:

        lookup = (
            RuleLibrary
            .rule_to_lookup_table(rule_number)
        )

        old_state = self.state

        new_state = [0] * self.width

        for i in range(self.width):

            left = old_state[
                (i - 1) % self.width
            ]

            center = old_state[i]

            right = old_state[
                (i + 1) % self.width
            ]

            neighborhood = (
                str(left)
                + str(center)
                + str(right)
            )

            new_state[i] = int(
                lookup[neighborhood]
            )

        self.state = new_state

        self.rule_history.append(
            rule_number
        )

        if store_history:
            self.history.append(
                new_state.copy()
            )

        return new_state

    def run_with_rules(
        self,
        rule_sequence: List[int],
        store_history: bool = True
    ) -> List[List[int]]:

        for rule in rule_sequence:

            self.step(
                rule,
                store_history=store_history
            )

        return self.history


class UniformCA:
    """CA using the same rule for every generation."""

    def __init__(
        self,
        width: int,
        rule_number: int,
        seed_state: Optional[List[int]] = None
    ):

        self.width = width
        self.rule_number = rule_number

        if seed_state is None:

            self.state = [0] * width
            self.state[
                width // 2
            ] = 1

        else:

            self.state = list(seed_state)

        self.lookup = (
            RuleLibrary
            .rule_to_lookup_table(
                rule_number
            )
        )

        self.history = [
            self.state.copy()
        ]

    def step(self):

        old_state = self.state

        new_state = [0] * self.width

        for i in range(self.width):

            left = old_state[
                (i - 1) % self.width
            ]

            center = old_state[i]

            right = old_state[
                (i + 1) % self.width
            ]

            neighborhood = (
                str(left)
                + str(center)
                + str(right)
            )

            new_state[i] = int(
                self.lookup[neighborhood]
            )

        self.state = new_state

        self.history.append(
            new_state.copy()
        )

        return new_state

    def run(self, steps: int):

        for _ in range(steps):
            self.step()

        return self.history


if __name__ == "__main__":

    print("=" * 60)
    print("Uniform CA - Rule 30")
    print("=" * 60)

    ca = UniformCA(
        width=31,
        rule_number=30
    )

    ca.run(15)

    for row in ca.history:
        print(
            "".join(
                str(cell)
                for cell in row
            )
        )
        