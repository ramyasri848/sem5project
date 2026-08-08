"""
experiments.py

Module 10b: Experiment Framework

Runs the complete sem5project pipeline and evaluates
the generated binary sequences.
"""

import argparse
import csv
import os
import time

from prng import KnuthCA_PRNG
from statistics import summary_report
from nist import run_all_tests

from visualization import (
    plot_ca_spacetime,
    plot_bit_distribution,
    plot_autocorrelation,
    plot_rule_usage
)


class ExperimentRunner:

    def __init__(
        self,
        ca_size: int = 101
    ):

        self.ca_size = ca_size

    def run_single_experiment(
        self,
        seed: int,
        iterations: int
    ):

        start = time.time()

        generator = KnuthCA_PRNG(
            seed=seed,
            ca_width=self.ca_size,
            extraction_method="full_state"
        )

        bits = generator.generate(
            iterations=iterations,
            store_history=True
        )

        elapsed = (
            time.time()
            - start
        )

        basic_stats = summary_report(
            bits
        )

        nist_results = run_all_tests(
            bits
        )

        return {
            "seed": seed,
            "ca_size": self.ca_size,
            "iterations": iterations,
            "bits": bits,
            "time": elapsed,
            "basic_stats": basic_stats,
            "nist_results": nist_results,
            "rule_sequence":
                generator.rule_sequence,
            "ca_history":
                generator.ca.history
        }

    def run_multiple_experiments(
        self,
        number_of_experiments: int,
        iterations: int,
        show_progress: bool = True
    ):

        results = []

        for i in range(
            number_of_experiments
        ):

            seed = 12345 + i

            if show_progress:

                print(
                    f"\nRunning experiment "
                    f"{i + 1}/"
                    f"{number_of_experiments}..."
                )

            result = (
                self.run_single_experiment(
                    seed=seed,
                    iterations=iterations
                )
            )

            results.append(result)

            if show_progress:

                print(
                    f"Completed in "
                    f"{result['time']:.2f} seconds"
                )

        return results


def print_results(
    results
):

    for index, result in enumerate(
        results,
        1
    ):

        stats = result[
            "basic_stats"
        ]

        monobit = stats[
            "monobit"
        ]

        runs = stats[
            "runs"
        ]

        print(
            f"\n{'=' * 60}"
        )

        print(
            f"Experiment {index}"
        )

        print(
            f"{'=' * 60}"
        )

        print(
            f"Seed             : "
            f"{result['seed']}"
        )

        print(
            f"CA Size          : "
            f"{result['ca_size']}"
        )

        print(
            f"Iterations       : "
            f"{result['iterations']:,}"
        )

        print(
            f"Generated Bits   : "
            f"{len(result['bits']):,}"
        )

        print(
            f"Time             : "
            f"{result['time']:.2f} seconds"
        )

        print(
            "\nStatistical Results"
        )

        print(
            f"Entropy          : "
            f"{stats['entropy']:.6f}"
        )

        print(
            f"Autocorrelation  : "
            f"{stats['autocorrelation']:.6f}"
        )

        print(
            f"Ones             : "
            f"{monobit['ones']:,}"
        )

        print(
            f"Zeros            : "
            f"{monobit['zeros']:,}"
        )

        print(
            f"Proportion Ones  : "
            f"{monobit['proportion_ones']:.6f}"
        )

        print(
            f"Monobit Statistic: "
            f"{monobit['statistic']:.6f}"
        )

        print(
            f"Runs             : "
            f"{runs['runs']:,}"
        )

        print(
            f"Expected Runs    : "
            f"{runs['expected_runs']:.3f}"
        )

        print(
            f"Runs Statistic   : "
            f"{runs['statistic']:.6f}"
        )

        print(
            f"Runs Valid       : "
            f"{runs['valid']}"
        )

        print(
            "\nNIST-style Tests"
        )

        for name, test in result[
            "nist_results"
        ].items():

            p_value = test.get(
                "p_value"
            )

            passed = test.get(
                "pass"
            )

            if p_value is None:

                print(
                    f"{name:25}: "
                    f"Not enough data"
                )

            else:

                print(
                    f"{name:25}: "
                    f"p={p_value:.6f} "
                    f"pass={passed}"
                )


def save_csv(
    results,
    filename
):

    os.makedirs(
        os.path.dirname(filename),
        exist_ok=True
    )

    with open(
        filename,
        "w",
        newline=""
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "experiment",
            "seed",
            "ca_size",
            "iterations",
            "bits",
            "entropy",
            "autocorrelation",
            "ones",
            "zeros",
            "proportion_ones",
            "monobit_statistic",
            "runs",
            "expected_runs",
            "runs_statistic",
            "time"
        ])

        for i, result in enumerate(
            results,
            1
        ):

            stats = result[
                "basic_stats"
            ]

            monobit = stats[
                "monobit"
            ]

            runs = stats[
                "runs"
            ]

            writer.writerow([
                i,
                result["seed"],
                result["ca_size"],
                result["iterations"],
                len(result["bits"]),
                stats["entropy"],
                stats["autocorrelation"],
                monobit["ones"],
                monobit["zeros"],
                monobit["proportion_ones"],
                monobit["statistic"],
                runs["runs"],
                runs["expected_runs"],
                runs["statistic"],
                result["time"]
            ])


def save_visualizations(
    result
):

    os.makedirs(
        "outputs",
        exist_ok=True
    )

    seed = result["seed"]

    plot_ca_spacetime(
        result["ca_history"],
        save_path=
        f"outputs/ca_spacetime_seed{seed}.png"
    )

    plot_bit_distribution(
        result["bits"],
        save_path=
        f"outputs/bit_distribution_seed{seed}.png"
    )

    plot_autocorrelation(
        result["bits"],
        save_path=
        f"outputs/autocorrelation_seed{seed}.png"
    )

    plot_rule_usage(
        result["rule_sequence"],
        save_path=
        f"outputs/rule_usage_seed{seed}.png"
    )


def main():

    parser = argparse.ArgumentParser(
        description=
        "sem5project Experiment Framework"
    )

    parser.add_argument(
        "--ca-size",
        type=int,
        default=101
    )

    parser.add_argument(
        "--iterations",
        type=int,
        default=100
    )

    parser.add_argument(
        "--experiments",
        type=int,
        default=3
    )

    args = parser.parse_args()

    print(
        "\n"
        "========================================\n"
        "       sem5project Experiment Framework\n"
        "========================================"
    )

    print(
        "\nExperiment Configuration"
    )

    print(
        f"\nStarting Seed       : 12345"
    )

    print(
        f"CA Size             : "
        f"{args.ca_size}"
    )

    print(
        f"Iterations          : "
        f"{args.iterations:,}"
    )

    print(
        f"Experiments         : "
        f"{args.experiments}"
    )

    bits_per_experiment = (
        args.ca_size
        * args.iterations
    )

    total_bits = (
        bits_per_experiment
        * args.experiments
    )

    print(
        f"Bits / Experiment   : "
        f"{bits_per_experiment:,}"
    )

    print(
        f"Total Bits          : "
        f"{total_bits:,}"
    )

    runner = ExperimentRunner(
        ca_size=args.ca_size
    )

    results = (
        runner.run_multiple_experiments(
            number_of_experiments=
            args.experiments,
            iterations=args.iterations,
            show_progress=True
        )
    )

    print_results(results)

    os.makedirs(
        "data/experiment_results",
        exist_ok=True
    )

    csv_file = (
        "data/experiment_results/"
        "experiment_results.csv"
    )

    save_csv(
        results,
        csv_file
    )

    print(
        f"\nCSV File: {csv_file}"
    )

    # Save plots only for first experiment
    save_visualizations(
        results[0]
    )

    print(
        "\nVisualization files saved "
        "to outputs/"
    )

    print(
        "\nExperiment completed successfully."
    )


if __name__ == "__main__":
    main()