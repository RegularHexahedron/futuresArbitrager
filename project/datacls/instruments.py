# datacls/instruments.py

"""
Docstring for datacls.instruments
"""

from dataclasses import dataclass
from typing import TypedDict

@dataclass(frozen=True)
class InstrumentPairs(TypedDict):
    equity: str
    futures: list[str]