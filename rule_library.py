"""
rule_library.py

Module 4: Cellular Automata Rule Library
"""

from typing import Dict, List


class RuleLibrary:
    """Curated Elementary Cellular Automata rules."""

    RULES: Dict[int, Dict] = {

        30: {
            "class": "III",
            "desc": "Chaotic"
        },

        45: {
            "class": "III",
            "desc": "Chaotic"
        },

        60: {
            "class": "II",
            "desc": "Additive"
        },

        90: {
            "class": "II",
            "desc": "Sierpinski triangle"
        },

        105: {
            "class": "II",
            "desc": "Additive"
        },

        110: {
            "class": "IV",
            "desc": "Complex / edge-of-chaos"
        },

        150: {
            "class": "II",
            "desc": "Additive"
        },

        165: {
            "class": "III",
            "desc": "Chaotic"
        },

        180: {
            "class": "III",
            "desc": "Chaotic"
        },

        225: {
            "class": "I",
            "desc": "Simple / fixed-point"
        },
    }

    def __init__(self):
        self.rule_numbers = list(
            self.RULES.keys()
        )

    def all_rules(self) -> List[int]:
        return self.rule_numbers.copy()

    def get_rules_by_class(
        self,
        ca_class: str
    ) -> List[int]:

        return [
            rule
            for rule, metadata in self.RULES.items()
            if metadata["class"] == ca_class
        ]

    def get_description(
        self,
        rule_number: int
    ) -> str:

        return self.RULES.get(
            rule_number,
            {}
        ).get(
            "desc",
            "Unknown rule"
        )

    @staticmethod
    def rule_to_lookup_table(
        rule_number: int
    ) -> Dict[str, str]:

        if not 0 <= rule_number <= 255:
            raise ValueError(
                "Rule number must be between 0 and 255."
            )

        binary = format(
            rule_number,
            "08b"
        )

        neighborhoods = [
            "111",
            "110",
            "101",
            "100",
            "011",
            "010",
            "001",
            "000"
        ]

        return dict(
            zip(
                neighborhoods,
                binary
            )
        )


if __name__ == "__main__":

    library = RuleLibrary()

    print("Available rules:")
    print(library.all_rules())

    print("\nRule 110:")
    print(
        library.rule_to_lookup_table(110)
    )