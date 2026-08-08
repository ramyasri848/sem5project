"""
config.py

Global configuration for sem5project.
"""

from dataclasses import dataclass


@dataclass
class Config:

    seed: int = 12345

    ca_width: int = 101

    iterations: int = 100

    extraction_method: str = "full_state"

    modulus: int = 2 ** 32

    experiments: int = 3


DEFAULT_CONFIG = Config()