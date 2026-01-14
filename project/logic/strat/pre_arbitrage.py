# logic/strat/pre_arbitrage.py

"""
Docstring for logic.strat.pre_arbitrage
"""

from datacls.rates import PreArbitrage
PRE_ARBITRAGE: dict[tuple[str, str], PreArbitrage] = {}

from utils.instruments import MATURITY_DATES
from utils.dates import compute_time_to_maturity, SECONDS_PER_YEAR
from datetime import timedelta
from logic.strat.rates import IMPLICIT_RATES
from utils.print import print_prearb


def update_pre_arb(updated_symbol: str) -> None:
    """
    Updates prearbitrage list after a symbol is updated by
    deleting old entries and recomputing new ones and
    prints them.

    Args:
        updated_symbol (str):
    """

    # global PRE_ARBITRAGE (just mutating)

    # Remove previous pre-arbitrage opportunities related to the symbol.
    to_delete = [
        pair
        for pair in PRE_ARBITRAGE
        if updated_symbol in pair
    ]
    for pair in to_delete:
        del PRE_ARBITRAGE[pair]

    # Recompute pre-arbitrage opportunities against all other symbols.
    for other_symbol in IMPLICIT_RATES:
        if other_symbol == updated_symbol:
            continue

        # Updated_symbol borrows, other_symbol lends.
        opp = compute_pre_arb(updated_symbol, other_symbol)
        if opp is not None:
            PRE_ARBITRAGE[(updated_symbol, other_symbol)] = opp
            print_prearb(opp)

        # other_symbol borrows, updated_symbol lends.
        opp = compute_pre_arb(other_symbol, updated_symbol)
        if opp is not None:
            PRE_ARBITRAGE[(other_symbol, updated_symbol)] = opp
            print_prearb(opp)


def compute_pre_arb(
    borrow_symbol: str,
    lend_symbol: str,
    time_tolerance: timedelta = timedelta()
    ) -> PreArbitrage | None:
    """
    For a futures pair, checks if
    - lender's maturity date is prior to borrower's
    - the difference of net interest rates is favorable
    Returns None if either condition is not fulfilled.

    Args:
        borrow_symbol (str):
        lend_symbol (str):
        time_tolerance (timedelta, optional):  difference between the maturity dates of the lending and borrowing futures. Defaults to timedelta().

    Returns:
        PreArbitrage | None:
    """

    b = IMPLICIT_RATES[borrow_symbol]
    l = IMPLICIT_RATES[lend_symbol]

    # Validate interest rates non-emptyness.
    if (
        b["borrower_rate"] is None or
        l["lender_rate"] is None or
        b["borrower_amount"] is None or
        b["borrower_amount"] == 0 or
        l["lender_amount"] is None or
        l["lender_amount"] == 0 or
        b["equity_bid"] is None or
        l["equity_ask"] is None
    ):
        return None

    # Compute times to maturity.
    ttm_borrower = compute_time_to_maturity(MATURITY_DATES[borrow_symbol])
    ttm_lender = compute_time_to_maturity(MATURITY_DATES[lend_symbol])

    # Check net interest rates.
    if (
        b["borrower_rate"] * ttm_borrower
        >=
        l["lender_rate"] * ttm_lender
    ):
        return None

    # Check maturity dates.
    if (
        ttm_lender * SECONDS_PER_YEAR + time_tolerance.total_seconds()
        >
        ttm_borrower * SECONDS_PER_YEAR
    ):
        return None

    pre_arb: PreArbitrage = {
        "lender_symbol": lend_symbol,
        "lender_ttm": ttm_borrower,
        "lender_rate": l["lender_rate"],
        "equity_ask": l["equity_ask"],
        "lend_amount": l["lender_amount"],
        "borrower_symbol": borrow_symbol,
        "borrower_ttm": ttm_lender,
        "borrower_rate": b["borrower_rate"],
        "equity_bid": b["equity_bid"],
        "borrow_amount": b["borrower_amount"],
    }

    return pre_arb