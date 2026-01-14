# logic/equity_spot.py

"""
Retrives underlying data.
"""

from datacls.bid_offer import BestBidOffer, BidOffer
from utils.instruments import YFINANCE_TICKERS
from yfinance import Ticker


def get_equity_bbo(equity_symbol: str) -> BestBidOffer:
    """
    Gets the best bid/offer for the requested asset from Yahoo Finance.
    NOTE: Ignores bid/ask spread for the spot price and overflows liquidity.
    
    :param equity_symbol:
    :type equity_symbol: str
    :return:
    :rtype: BestBidOffer
    """
    
    ticker = YFINANCE_TICKERS[equity_symbol]
    last_price = Ticker(ticker).fast_info["lastPrice"]

    bbo = BestBidOffer(
        best_bid = BidOffer(price = last_price, size = 100000),
        best_offer = BidOffer(price = last_price, size = 100000)
    )

    return bbo