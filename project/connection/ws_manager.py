# connection/ws_manager.py

"""
Defines connection with the WebSocket.
"""

from datacls.websocket import MdMsg
from datacls.bid_offer import BestBidOffer, BidOffer, EventFutureBBO
from utils.queue import EVENT_QUEUE

from pyRofex import MarketDataEntry, market_data_subscription
from utils.instruments import FUTURES

from pyRofex import init_websocket_connection
from utils.config import ENVIRONMENT

from pyRofex import close_websocket_connection

def init_websocket():
    """
    Initializes a websocket connection by:
    - defining the handlers and
    - subscribing to the futures of interest.
    """

    # pyRofex's websocket implicitly uses "time" but has to be imported manually...
    import time

    def market_data_handler(msg: MdMsg):
        """
        Parses market data message into an event of EventFutureBBO class and 
        Sends it to the event queue.

        Args:
            msg (MdMsg): market data message from the websocket
        """

        # Retrive relevant information.
        future_symbol = msg["instrumentId"]["symbol"]
        md: dict[str, list[BidOffer]] = msg["marketData"]
        future_bbo: BestBidOffer = {
            "best_bid": md["BI"][0] if md["BI"] else None, 
            "best_offer": md["OF"][0] if md["OF"] else None
            }
        timestamp = msg["timestamp"]

        # Construct the event.
        event = EventFutureBBO(
            future_symbol, future_bbo, timestamp
        )

        # Send event to queue.
        EVENT_QUEUE.put_nowait(event)
        
    def exception_handler(e: Exception):

        EVENT_QUEUE.put_nowait(e)

    def error_handler(msg: str):
        print(f"Error Message Received: {msg}")


    init_websocket_connection(
        market_data_handler = market_data_handler,
        error_handler = error_handler,
        exception_handler = exception_handler,
        environment = ENVIRONMENT
        )
    
    """ Market Data Subscription. """
    entries = [
        MarketDataEntry.BIDS,
        MarketDataEntry.OFFERS,
        ]

    market_data_subscription(
        tickers = FUTURES,
        entries = entries,
        depth = 1
        )

def close_websocket():
    try:
        close_websocket_connection()
    except Exception as e:
        raise e
    else:
        print()
        print("Websocket connection closed.")