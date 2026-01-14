# utils/instruments.py

"""
Defines the instruments of interst.
"""

from datacls.instruments import InstrumentPairs
from datetime import datetime

# FIXME?: HARDCODED
INSTRUMENTS: list[InstrumentPairs] = [
    {
        "equity": "GGAL",
        "futures": ["GGAL/FEB26", "GGAL/ABR26"]
    },
    {
        "equity": "PAMP",
        "futures": ["PAMP/FEB26", "PAMP/ABR26"]
    },
    {
        "equity": "YPFD",
        "futures": ["YPFD/FEB26", "YPFD/ABR26"]
    },
    {
        "equity": "DLR/SPOT",
        "futures": ["DLR/FEB26", "DLR/ABR26"]
    },
]

# FIXME?: HARDCODED
MATURITY_DATES: dict[str, datetime] = {
    "GGAL/FEB26": datetime(2026, 2, 26, 0, 0),
    "GGAL/ABR26": datetime(2026, 4, 29, 0, 0),
    "YPFD/FEB26": datetime(2026, 2, 26, 0, 0),
    "YPFD/ABR26": datetime(2026, 4, 29, 0, 0),
    "PAMP/FEB26": datetime(2026, 2, 26, 0, 0),
    "PAMP/ABR26": datetime(2026, 4, 29, 0, 0),
    "DLR/FEB26": datetime(2026, 2, 27, 0, 0),
    "DLR/ABR26": datetime(2026, 4, 30, 0, 0),
}

FUTURE_TO_EQUITY: dict[str, str] = {
    future: instrument["equity"]
    for instrument in INSTRUMENTS
    for future in instrument["futures"]
}

FUTURES: list[str] = [
    future
    for instrument in INSTRUMENTS
    for future in instrument["futures"]
]

YFINANCE_TICKERS = {
    "GGAL": "GGAL.BA",
    "PAMP": "PAMP.BA",
    "YPFD": "YPFD.BA",
    "DLR/SPOT": "ARS=X"
}

CONTRACT_MULTIPLIER = 100







# TODO: Something like this is cleaner.
INSTRUMENTS2: list[dict[str, str | datetime | int]] = [
    {
        "equity_symbol": "GGAL",
        "yfinance_symbol": "GGAL.BA",
        "future_symbol": "GGAL/FEB26",
        "maturity_date": datetime(2026, 2, 26, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 1000,
        "contractMultiplier": 100,
        "roundLot": 1
    },
    {
        "equity_symbol": "GGAL",
        "yfinance_symbol": "GGAL.BA",
        "future_symbol": "GGAL/ABR26",
        "maturity_date": datetime(2026, 4, 29, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 1000,
        "contractMultiplier": 100,
        "roundLot": 1
    },
    {
        "equity_symbol": "PAMP",
        "yfinance_symbol": "PAMP.BA",
        "future_symbol": "PAMP/FEB26",
        "maturity_date": datetime(2026, 2, 26, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 2000,
        "contractMultiplier": 100,
        "roundLot": 1
    },
    {
        "equity_symbol": "PAMP",
        "yfinance_symbol": "PAMP.BA",
        "future_symbol": "PAMP/ABR26",
        "maturity_date": datetime(2026, 4, 29, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 1000,
        "contractMultiplier": 100,
        "roundLot": 1
    },
    {
        "equity_symbol": "YPFD",
        "yfinance_symbol": "YPFD.BA",
        "future_symbol": "YPFD/FEB26",
        "maturity_date": datetime(2026, 2, 26, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 1000,
        "contractMultiplier": 100,
        "roundLot": 1
    },
    {
        "equity_symbol": "YPFD",
        "yfinance_symbol": "YPFD.BA",
        "future_symbol": "YPFD/ABR26",
        "maturity_date": datetime(2026, 4, 29, 0, 0),
        "minTradeVol": 1,
        "maxTradeVol": 1000,
        "contractMultiplier": 100,
        "roundLot": 1
    }
]


