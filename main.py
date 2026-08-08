"""
main.py

Entry point for sem5project.
"""

from config import DEFAULT_CONFIG
from experiments import ExperimentRunner


def main():

    runner = ExperimentRunner(
        ca_size=DEFAULT_CONFIG.ca_width
    )

    results = runner.run_multiple_experiments(
        number_of_experiments=
        DEFAULT_CONFIG.experiments,

        iterations=
        DEFAULT_CONFIG.iterations,

        show_progress=True
    )

    print(
        "\nsem5project completed."
    )


if __name__ == "__main__":
    main()