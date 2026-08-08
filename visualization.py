"""
visualization.py

Module 10: Visualization

Creates:
    1. CA space-time diagram
    2. Bit distribution
    3. Autocorrelation plot
    4. Rule usage plot
"""

import matplotlib.pyplot as plt
from collections import Counter
from typing import List


def plot_ca_spacetime(
    history,
    save_path=None
):

    if not history:
        return

    plt.figure(
        figsize=(12, 7)
    )

    plt.imshow(
        history,
        cmap="binary",
        interpolation="nearest",
        aspect="auto"
    )

    plt.title(
        "KnuthCA Cellular Automata Evolution"
    )

    plt.xlabel(
        "Cell Position"
    )

    plt.ylabel(
        "Generation"
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=150
        )

    plt.close()


def plot_bit_distribution(
    bits: List[int],
    save_path=None
):

    zeros = bits.count(0)
    ones = bits.count(1)

    plt.figure(
        figsize=(7, 5)
    )

    plt.bar(
        ["0", "1"],
        [zeros, ones]
    )

    plt.title(
        "Generated Bit Distribution"
    )

    plt.xlabel(
        "Bit"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=150
        )

    plt.close()


def plot_autocorrelation(
    bits: List[int],
    save_path=None,
    max_lag: int = 50
):

    if len(bits) < 2:
        return

    x = [
        1 if bit == 1 else -1
        for bit in bits
    ]

    n = len(x)

    mean = sum(x) / n

    denominator = sum(
        (value - mean) ** 2
        for value in x
    )

    if denominator == 0:
        return

    lags = []
    correlations = []

    max_lag = min(
        max_lag,
        n - 1
    )

    for lag in range(
        1,
        max_lag + 1
    ):

        numerator = sum(
            (x[i] - mean)
            * (x[i + lag] - mean)
            for i in range(
                n - lag
            )
        )

        correlation = (
            numerator
            / denominator
        )

        lags.append(lag)
        correlations.append(
            correlation
        )

    plt.figure(
        figsize=(10, 5)
    )

    plt.plot(
        lags,
        correlations,
        marker="o",
        markersize=3
    )

    plt.axhline(
        0,
        linestyle="--"
    )

    plt.title(
        "Bitstream Autocorrelation"
    )

    plt.xlabel(
        "Lag"
    )

    plt.ylabel(
        "Correlation"
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=150
        )

    plt.close()


def plot_rule_usage(
    rule_sequence,
    save_path=None
):

    if not rule_sequence:
        return

    counts = Counter(
        rule_sequence
    )

    rules = sorted(
        counts.keys()
    )

    values = [
        counts[rule]
        for rule in rules
    ]

    plt.figure(
        figsize=(10, 5)
    )

    plt.bar(
        [str(rule) for rule in rules],
        values
    )

    plt.title(
        "Adaptive CA Rule Usage"
    )

    plt.xlabel(
        "CA Rule"
    )

    plt.ylabel(
        "Number of Generations"
    )

    plt.tight_layout()

    if save_path:
        plt.savefig(
            save_path,
            dpi=150
        )

    plt.close()


if __name__ == "__main__":

    print(
        "Visualization module loaded successfully."
    )