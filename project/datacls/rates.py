# datacls/rates.py

"""
Docstring for datacls.rates
"""

from dataclasses import dataclass
from typing import TypedDict

@dataclass
class InterestRates(TypedDict):
    time_to_maturity: float
    lender_rate: float | None
    lender_amount: int | None       # contracts amount
    equity_ask: float | None
    borrower_rate: float | None
    borrower_amount: int | None     # contracts amount
    equity_bid: float | None

@dataclass
class PreArbitrage(TypedDict):
    lender_symbol: str
    lender_ttm: float
    lender_rate: float
    equity_ask: float
    lend_amount: int                # contracts amount
    borrower_symbol: str
    borrower_ttm: float
    borrower_rate: float
    equity_bid: float
    borrow_amount: int              # contracts amount

@dataclass
class BestArb(TypedDict):
    lender_symbol: str
    total_lent: float
    bought_eq_bid: float
    bought_eq_amount: int           # underlying amount
    lending_rate: float
    lending_return: float
    borrower_symbol: str
    total_borrowed: float
    sold_eq_ask: float
    sold_eq_amount: int             # underlying amount
    borrowing_rate: float
    borrowing_cost: float
    excess: float
    pnl: float