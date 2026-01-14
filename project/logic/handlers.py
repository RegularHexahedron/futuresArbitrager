# logic/handlers.py

"""
Excecutes the main logic of the program.
"""

from datetime import datetime
from datacls.bid_offer import EventFutureBBO
from utils.print import print_bbo
from utils.instruments import FUTURE_TO_EQUITY, MATURITY_DATES
from logic.equity_spot import get_equity_bbo
from utils.dates import compute_time_to_maturity
from logic.strat.rates import update_rates
from logic.strat.pre_arbitrage import PRE_ARBITRAGE, update_pre_arb
from logic.strat.arbitrage import compute_arbitrage


def handle_future(event: EventFutureBBO) -> None:
    """
    Handles the recieve of a market data update on the bids/offers of a future and
    Runs the whole strategy.

    Args:
        event (EventFutureBBO): parsed market data update.
    """

    print("---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----")
    print(f"---- {datetime.fromtimestamp(event.timestamp/1000).isoformat()} -- ---- ---- ---- ---- ---- ---- ---- ---- ----")
    print("---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ---- ----")

    # Print future's book update.
    print(f"Update on {event.future_symbol}:")
    print_bbo(event.future_bbo)

    # Compute future's time to maturity.
    time_to_maturity = compute_time_to_maturity(MATURITY_DATES[event.future_symbol])

    # Get and print underlying's asset book.
    equity_symbol = FUTURE_TO_EQUITY[event.future_symbol]
    equity_bbo = get_equity_bbo(equity_symbol)
    print("Equity:")
    print_bbo(equity_bbo)
    
    # Update implicit interest rates dictionary with the new rate and prints it.
    update_rates(event.future_symbol, event.future_bbo, equity_bbo, time_to_maturity)

    # Update pre-arbitrage opportunities dictionary.
    update_pre_arb(event.future_symbol)
    
    # Determine and print arbitrage oportunities.
    if PRE_ARBITRAGE:
        compute_arbitrage()



import traceback

def handle_exception(event: Exception) -> None:
    str = "".join(
        traceback.format_exception(type(event), event, event.__traceback__)
    )
    print(str)









