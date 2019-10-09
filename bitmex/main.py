from bitmex.bitmex_websocket import BitMEXWebsocket
import logging
import time
from google.cloud import pubsub_v1
import os


project_id = "axon-249519"

publisher = pubsub_v1.PublisherClient() #.from_service_account_file(os.environ['GOOGLE_APPLICATION_CREDENTIALS'])

# Basic use of websocket.
def run():
    logger = setup_logger()

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="https://www.bitmex.com/api/v1", symbol="XBTUSD",
                         api_key=None, api_secret=None)

    logger.info("Instrument data: %s" % ws.get_instrument())

    # Run forever
    while ws.ws.sock.connected:
        # print(ws.data.keys())

        # Ticker
        logger.info("Ticker: %s" % str(ws.get_ticker()).replace("'",'"'))
        publisher.publish(publisher.topic_path(project_id, "ticker"), data=str(ws.get_ticker()).replace("'",'"').encode('utf-8'))

        # Trades
        # logger.info("Recent Trades: %s\n\n" % str(ws.recent_trades()).replace("'",'"'))
        # publisher.publish(publisher.topic_path(project_id, "recentTrades"), data=str(ws.recent_trades()).replace("'",'"').encode('utf-8'))

        # Depth
        # if "orderBookL2" in ws.data:
        #     logger.info("Market Depth: %s" % str(ws.market_depth()).replace("'",'"'))
        #     publisher.publish(publisher.topic_path(project_id, "orderBookL2"), data=str(ws.market_depth()).replace("'", '"').encode('utf-8'))


def setup_logger():
    # Prints logger info to terminal
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # Change this to DEBUG if you want a lot more info
    ch = logging.StreamHandler()
    # create formatter
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    # add formatter to ch
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


if __name__ == "__main__":
    run()
