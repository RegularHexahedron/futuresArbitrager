# utils/print.py

"""
Print helpers.
"""

from datacls.bid_offer import BestBidOffer
from datacls.rates import InterestRates, PreArbitrage, BestArb
from utils.instruments import CONTRACT_MULTIPLIER

def print_bbo(bbo: BestBidOffer) -> None:

    bb_price, bb_size = (
        (bbo["best_bid"]["price"], bbo["best_bid"]["size"])
        if bbo["best_bid"] is not None
        else (None, None)
    )
    bo_price, bo_size = (
        (bbo["best_offer"]["price"], bbo["best_offer"]["size"])
        if bbo["best_offer"] is not None
        else (None, None)
    )
    bb_price_str = (
        f"{bb_price:.2f}"
        if bb_price is not None
        else "None"
    )
    bb_size_str = (
        f"{bb_size}"
        if bb_size is not None
        else "None"
    )
    bo_price_str = (
        f"{bo_price:.2f}"
        if bo_price is not None
        else "None"
    )
    bo_size_str = (
        f"{bo_size}"
        if bo_size is not None
        else "None"
    )
    print(
        f"    "
        f"BB @ {bb_price_str} ({bb_size_str})"
        f" | "
        f"BO @ {bo_price_str} ({bo_size_str})"
    )


def print_rates(interest_rates: InterestRates) -> None:
    """
    Prints interest rates (in percentages).
    """

    lender_rate = (
        interest_rates["lender_rate"] * 100
        if interest_rates["lender_rate"] is not None
        else None
    )
    lender_amount = interest_rates["lender_amount"]
    borrower_rate = (
        interest_rates["borrower_rate"] * 100
        if interest_rates["borrower_rate"] is not None
        else None
    )
    borrower_amount = interest_rates["borrower_amount"]

    lender_rate_str = (
        f"{lender_rate:.2f}"
        if lender_rate is not None
        else "None"
    )
    lender_amount_str = (
        lender_amount
        if lender_amount is not None
        else "None"
    )
    borrower_rate_str = (
        f"{borrower_rate:.2f}"
        if borrower_rate is not None
        else "None"
    )
    borrower_amount_str = (
        borrower_amount
        if borrower_amount is not None
        else "None"
    )
    print(f"New (annualized) rates:")
    print(
        f"    "
        f"Lend: {lender_rate_str}% ({lender_amount_str} contracts)"
        f" | "
        f"Borrow: {borrower_rate_str}% ({borrower_amount_str} contracts)"
    )


def print_prearb(prearb: PreArbitrage):

    print(
        f"New pre-arb: "
        f"Lend: {prearb["lender_symbol"]}"
        f" | "
        f"Borrow: {prearb["borrower_symbol"]}"
    )

    r_lend = prearb["lender_rate"]
    assert r_lend is not None
    r_lend_100 = r_lend * 100
    a_lend = prearb["lend_amount"]
    eq_ask = prearb["equity_ask"]

    r_borr = prearb["borrower_rate"]
    assert r_borr is not None
    r_borr_100 = r_borr * 100
    a_borr = prearb["borrow_amount"]
    eq_bid = prearb["equity_bid"]

    print(
        f"    "
        f"Lend: {r_lend_100:.2f}% for ({a_lend} contracts) @ {eq_ask}"
        f" | "
        f"Borrow: {r_borr_100:.2f}% for ({a_borr} contracts) @ {eq_bid}"
    )


def print_bestarb(best: BestArb):

        print("________________________________________________________________________________")
        print("| | | |")
        print(f"| | | | "
            f"NEW ARBITRAGE: "
            f"Lend {best["lender_symbol"]}"
            f" | "
            f"Borrow: {best["borrower_symbol"]}"
        )
        print(f"| | | | "
            f"    Borrow:"
        )
        print(f"| | | | "
            f"        "
            f"Sell ({best["sold_eq_amount"]}) of underlying {best["sold_eq_ask"]} and "
            f"Buy ({best["sold_eq_amount"]/CONTRACT_MULTIPLIER}) of {best["borrower_symbol"]}"
        )
        print(f"| | | | "
            f"        "
            f"Total Borrowed: {best["total_borrowed"]} "
            f"@ {(best["borrowing_rate"]*100):.2f}% per year "
            f"- {(best["borrowing_cost"]*100):.2f}% net"
        )
        print(f"| | | | "
            f"    Lend:"
        )
        print(f"| | | | "
            f"        "
            f"Buy {best["bought_eq_amount"]} of underlying @ {best["bought_eq_bid"]} and "
            f"Sell ({best["bought_eq_amount"]/CONTRACT_MULTIPLIER}) of {best["lender_symbol"]}")
        print(f"| | | | "
            f"        Total Lent: {best["total_lent"]} "
            f"@ {(best["lending_rate"]*100):.2f}% per year "
            f"- {(best["lending_return"]*100):.2f}% net")
        print(f"| | | | "
            f"    PnL: {best["pnl"]:.2f}"
        )
        print(f"| | | | ")
        print("________________________________________________________________________________")
