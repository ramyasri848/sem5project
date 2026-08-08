"""
nist.py

Module 9b: NIST-style statistical tests.

This implements a practical academic subset:
    - Frequency / Monobit
    - Block Frequency
    - Runs
    - Longest Run
    - Cumulative Sums
"""

import math
from typing import Dict, List

from statistics import (
    monobit_frequency,
    runs_test
)


def block_frequency_test(
    bits: List[int],
    block_size: int = 128
) -> Dict:

    n = len(bits)

    num_blocks = n // block_size

    if num_blocks == 0:

        return {
            "p_value": None,
            "pass": False,
            "reason": "Sequence too short"
        }

    chi_square = 0.0

    for i in range(num_blocks):

        block = bits[
            i * block_size:
            (i + 1) * block_size
        ]

        proportion = (
            sum(block)
            / block_size
        )

        chi_square += (
            proportion - 0.5
        ) ** 2

    chi_square *= (
        4 * block_size
    )

    p_value = _igamc(
        num_blocks / 2,
        chi_square / 2
    )

    return {
        "num_blocks": num_blocks,
        "chi_square": chi_square,
        "p_value": p_value,
        "pass": p_value >= 0.01
    }


def longest_run_test(
    bits: List[int]
) -> Dict:

    block_size = 8

    num_blocks = (
        len(bits)
        // block_size
    )

    if num_blocks == 0:

        return {
            "p_value": None,
            "pass": False
        }

    counts = {
        1: 0,
        2: 0,
        3: 0,
        4: 0
    }

    for i in range(num_blocks):

        block = bits[
            i * block_size:
            (i + 1) * block_size
        ]

        longest = _longest_run(
            block
        )

        if longest <= 1:
            counts[1] += 1

        elif longest == 2:
            counts[2] += 1

        elif longest == 3:
            counts[3] += 1

        else:
            counts[4] += 1

    probabilities = [
        0.2148,
        0.3672,
        0.2305,
        0.1875
    ]

    chi_square = 0.0

    for k in range(4):

        expected = (
            num_blocks
            * probabilities[k]
        )

        chi_square += (
            (
                counts[k + 1]
                - expected
            ) ** 2
            / expected
        )

    p_value = _igamc(
        1.5,
        chi_square / 2
    )

    return {
        "counts": counts,
        "chi_square": chi_square,
        "p_value": p_value,
        "pass": p_value >= 0.01
    }


def cumulative_sums_test(
    bits: List[int]
) -> Dict:

    n = len(bits)

    signed = [
        1 if bit == 1 else -1
        for bit in bits
    ]

    running = 0
    maximum = 0

    for value in signed:

        running += value

        maximum = max(
            maximum,
            abs(running)
        )

    if maximum == 0:

        return {
            "z_max": 0,
            "p_value": 0.0,
            "pass": False
        }

    z = maximum

    total = 0.0

    start = int(
        (-n / z + 1) / 4
    )

    end = int(
        (n / z - 1) / 4
    )

    for k in range(
        start,
        end + 1
    ):

        total += (
            _norm_cdf(
                ((4 * k + 1) * z)
                / math.sqrt(n)
            )
            -
            _norm_cdf(
                ((4 * k - 1) * z)
                / math.sqrt(n)
            )
        )

    p_value = max(
        0.0,
        min(
            1.0,
            1 - total
        )
    )

    return {
        "z_max": z,
        "p_value": p_value,
        "pass": p_value >= 0.01
    }


def run_all_tests(
    bits: List[int]
) -> Dict:

    return {

        "monobit":
            monobit_frequency(bits),

        "block_frequency":
            block_frequency_test(bits),

        "runs":
            runs_test(bits),

        "longest_run":
            longest_run_test(bits),

        "cumulative_sums":
            cumulative_sums_test(bits)
    }


def _longest_run(
    block: List[int]
) -> int:

    longest = 0
    current = 0

    for bit in block:

        if bit == 1:
            current += 1
            longest = max(
                longest,
                current
            )

        else:
            current = 0

    return longest


def _norm_cdf(
    x: float
) -> float:

    return 0.5 * (
        1
        + math.erf(
            x / math.sqrt(2)
        )
    )


def _igamc(
    a: float,
    x: float
) -> float:

    if x < 0 or a <= 0:
        return 0.0

    if x == 0:
        return 1.0

    if x < a + 1:
        return 1 - _igam_series(a, x)

    return _igam_continued_fraction(
        a,
        x
    )


def _igam_series(
    a: float,
    x: float
) -> float:

    ap = a

    total = 1.0 / a

    delta = total

    for _ in range(200):

        ap += 1

        delta *= x / ap

        total += delta

        if abs(delta) < abs(total) * 1e-12:
            break

    return (
        total
        * math.exp(
            -x
            + a * math.log(x)
            - math.lgamma(a)
        )
    )


def _igam_continued_fraction(
    a: float,
    x: float
) -> float:

    tiny = 1e-300

    b = x + 1 - a

    c = 1 / tiny

    d = 1 / b

    h = d

    for i in range(1, 200):

        an = -i * (i - a)

        b += 2

        d = an * d + b

        if abs(d) < tiny:
            d = tiny

        c = b + an / c

        if abs(c) < tiny:
            c = tiny

        d = 1 / d

        delta = d * c

        h *= delta

        if abs(delta - 1) < 1e-12:
            break

    return (
        math.exp(
            -x
            + a * math.log(x)
            - math.lgamma(a)
        )
        * h
    )