# logic/strat/rates.py

"""
Docstring for logic.strat.rates
"""

from datacls.rates import InterestRates
IMPLICIT_RATES: dict[str, InterestRates] = {}
from datacls.bid_offer import BestBidOffer
from utils.instruments import CONTRACT_MULTIPLIER
from utils.print import print_rates

from math import log

def update_rates(
    future_symbol: str,
    future_bbo: BestBidOffer,
    equity_bbo: BestBidOffer,
    time_to_maturity: float
    ) -> None:
    """
    Updates the implicit interest rates dictiornary and
    Prints the updated key properly formatted.

    Args:
        future_symbol (str):
        future_bbo (BestBidOffer):
        equity_bbo (BestBidOffer):
        time_to_maturity (float):
    """

    # global IMPLICIT_RATES (just mutating)

    IMPLICIT_RATES[future_symbol] = compute_implicit_rates(future_bbo, equity_bbo, time_to_maturity)
    print_rates(IMPLICIT_RATES[future_symbol])


def compute_implicit_rates(
    future_bbo: BestBidOffer,
    equity_bbo: BestBidOffer,
    time_to_maturity: float
    ) -> InterestRates:
    """
    Computes the implicit interest rates of the price of a future.

    Args:
        future_bbo (BestBidOffer):
        equity_bbo (BestBidOffer):
        time_to_maturity (float):

    Returns:
        InterestRates: dict
            "time_to_maturity: (float),
            "lender_rate": (float),
            "lender_amount": (int) amount of the UNDERLYING,
            "equity_ask": (float),
            "borrower_rate": (float),
            "borrower_amount": (int) amount of the UNDERLYING,
            "equity_bid": (float)
    """

    T = time_to_maturity
    fb, fa, eb, ea = future_bbo["best_bid"], future_bbo["best_offer"], \
        equity_bbo["best_bid"], equity_bbo["best_offer"]

    if fb is not None and ea is not None:
        r_lend = 1/T * log(fb["price"]/ea["price"])
        a_lend = int(min(fb["size"], ea["size"] / CONTRACT_MULTIPLIER))
        eap = ea["price"]
    else:
        r_lend = None
        a_lend = None
        if ea is not None:
            eap = ea["price"]
        else:
            eap = None

    if fa is not None and eb is not None:
        r_borr = 1/T * log(fa["price"]/eb["price"])
        a_borr = int(min(fa["size"], eb["size"] / CONTRACT_MULTIPLIER))
        ebp = eb["price"]
    else:
        r_borr = None
        a_borr = None
        if eb is not None:
            ebp = eb["price"]
        else:
            ebp = None

    interest_rates: InterestRates = {
        "time_to_maturity": time_to_maturity,
        "lender_rate": r_lend,
        "lender_amount": a_lend,
        "equity_ask": eap,
        "borrower_rate": r_borr,
        "borrower_amount": a_borr,
        "equity_bid": ebp
    }

    return interest_rates






