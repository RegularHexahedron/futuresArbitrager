# datacls/websocket.py

"""
Docstring for datacls.websocket
"""

from dataclasses import dataclass
from typing import TypedDict, Any

@dataclass
class InstrumentId(TypedDict):
    marketId: str
    symbol: str

@dataclass
class MdMsg(TypedDict):
    type: str
    timestamp: int
    instrumentId: InstrumentId
    marketData: dict

@dataclass
class IntrumentDetails(TypedDict):
    symbol: str | None
    segment: dict[str, str]
    lowLimitPrice: float
    highLimitPrice: float
    minPriceIncrement: float
    minTradeVol: float
    maxTradeVol: float
    tickSize: float
    contractMultiplier: float
    roundLot: float
    priceConvertionFactor: float
    maturityDate: str
    currency: str
    orderTypes: list[str]
    timesInForce: list[str]
    securityType: Any | None
    settlType: Any | None
    instrumentPricePrecision: int
    instrumentSizePrecision: int
    securityId: Any | None
    securityIdSource: Any | None
    securityDescription: str
    tickPriceRanges: dict[str, dict]
    strike: Any | None
    underlying: str
    cficode: str
    instrumentId: InstrumentId