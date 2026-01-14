# datacls/bid_offer.py

"""
Docstring for datacls.bid_offer
"""

from dataclasses import dataclass
from typing import TypedDict

@dataclass
class BidOffer(TypedDict):
    price: float
    size: int

@dataclass
class BestBidOffer(TypedDict):
    best_bid: BidOffer | None
    best_offer: BidOffer | None

@dataclass(frozen=True)
class EventFutureBBO:
    future_symbol: str
    future_bbo: BestBidOffer
    timestamp: int