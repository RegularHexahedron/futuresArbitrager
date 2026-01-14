# logic/strat/arbitrage.py

"""
Docstring for logic.strat.arbitrage
"""

from datacls.rates import BestArb
from logic.strat.pre_arbitrage import PRE_ARBITRAGE
from utils.instruments import CONTRACT_MULTIPLIER
from utils.print import print_bestarb

def compute_arbitrage() -> None:
    """
    Computes all possible arbitrage opportunities (and prints them if any).
    """

    for (borrow_symbol, lend_symbol), pre in PRE_ARBITRAGE.items():

        r_l = pre["lender_rate"]
        r_b = pre["borrower_rate"]

        T_l = pre["lender_ttm"]
        T_b = pre["borrower_ttm"]

        eq_l = pre["equity_bid"]
        eq_b = pre["equity_ask"]

        # In contracts.
        max_l = pre["lend_amount"]
        max_b = pre["borrow_amount"]

        best_pnl = 0.0
        best: BestArb | None = None

        for n_l in [x * CONTRACT_MULTIPLIER for x in range(1, max_l + 1)]:
            N_l = n_l * eq_l

            for n_b in [x * CONTRACT_MULTIPLIER for x in range(1, max_b + 1)]:
                N_b = n_b * eq_b
                if N_b < N_l:
                    continue

                pnl = N_l * r_l * T_l - N_b * r_b * T_b

                if pnl > best_pnl:
                    best_pnl = pnl
                    best = {
                        "lender_symbol": pre["lender_symbol"],
                        "total_lent": N_l,
                        "bought_eq_bid": eq_l,
                        "bought_eq_amount": n_l,
                        "lending_rate": r_l,
                        "lending_return": r_l * T_l,
                        "borrower_symbol": pre["borrower_symbol"],
                        "total_borrowed": N_b,
                        "sold_eq_ask": eq_b,
                        "sold_eq_amount": n_b,
                        "borrowing_rate": r_b,
                        "borrowing_cost": r_b * T_b,
                        "excess": N_b - N_l,
                        "pnl": pnl,
                    }

        if best is not None:
            print_bestarb(best)

    print("No further arbitrage opportunity detected.")
    print()
