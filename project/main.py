# main.py

"""

"""

import threading
STOP_EVENT = threading.Event()

import signal

def manual_stop(signal_number: int | None = None, frame = None):
    global STOP_EVENT
    STOP_EVENT.set()

# Ways of terminating the process.
signal.signal(signal.SIGINT, manual_stop)   # Ctrl + C
signal.signal(signal.SIGTERM, manual_stop)  # kill

from utils.queue import EVENT_QUEUE
from queue import Empty

from datacls.bid_offer import EventFutureBBO

def main():

    from connection.init import establish_connection
    from connection.ws_manager import init_websocket, close_websocket
    from logic.handlers import handle_future, handle_exception
    
    establish_connection()
    init_websocket()
    
    while not STOP_EVENT.is_set():
        try:
            # Timeout is so it loops every 1 second and can read if it's shutdown.
            event = EVENT_QUEUE.get(timeout=1)
        except Empty:
            continue
        else:
            if isinstance(event, EventFutureBBO):
                handle_future(event)
            elif isinstance(event, Exception):
                handle_exception(event)

    close_websocket()



if __name__ == "__main__":
    main()