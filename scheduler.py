"""
scheduler.py

Module 3: Adaptive Rule Scheduler

Arithmetic features determine which CA rule is selected.
"""

from typing import Dict, List

from rule_library import RuleLibrary


class AdaptiveRuleScheduler:

    def __init__(
        self,
        rule_library: RuleLibrary = None
    ):

        self.library = (
            rule_library
            if rule_library is not None
            else RuleLibrary()
        )

        self.rules = self.library.all_rules()

    def select_rule(
        self,
        features: Dict
    ) -> int:

        # Base rule from mod11.
        base_index = (
            features["mod11"]
            % len(self.rules)
        )

        candidate = self.rules[base_index]

        # If the arithmetic value is complex,
        # avoid Class I rules.
        if features["bit_transitions"] > 4:

            metadata = self.library.RULES[
                candidate
            ]

            if metadata["class"] == "I":

                class_iv = (
                    self.library
                    .get_rules_by_class("IV")
                )

                if class_iv:
                    candidate = class_iv[0]

        # Odd arithmetic values bias toward
        # chaotic Class III rules.
        if features["parity"] == "Odd":

            class_iii = (
                self.library
                .get_rules_by_class("III")
            )

            if class_iii:

                index = (
                    features["digit_sum"]
                    % len(class_iii)
                )

                candidate = class_iii[index]

        return candidate

    def select_rule_sequence(
        self,
        feature_vectors: List[Dict]
    ) -> List[int]:

        return [
            self.select_rule(features)
            for features in feature_vectors
        ]


if __name__ == "__main__":

    from arithmetic_features import (
        ArithmeticFeatureExtractor
    )

    extractor = ArithmeticFeatureExtractor()

    scheduler = AdaptiveRuleScheduler()

    print("=" * 60)
    print("Adaptive Rule Scheduler")
    print("=" * 60)

    for value in [
        2378,
        91,
        4096,
        777
    ]:

        features = (
            extractor.extract_features(value)
        )

        rule = scheduler.select_rule(
            features
        )

        print(
            f"value={value:6} -> rule={rule}"
        )