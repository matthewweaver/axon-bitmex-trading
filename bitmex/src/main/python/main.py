from bitmex_websocket import BitMEXWebsocket
import logging
import time
from google.cloud import pubsub_v1

project_id = "axon-249519"
topic_name = "orderbook"

# import os
# dirname = os.path.dirname(__file__)
# service_account = os.path.join(dirname, '../path/resources/axon-249519-6fec7265c5cf.json')

publisher = pubsub_v1.PublisherClient().from_service_account_file("/Users/emmahowes/Documents/Matt/git/axon-249519-6fec7265c5cf.json")
topic_path = publisher.topic_path(project_id, topic_name)

# Basic use of websocket.
def run():
    logger = setup_logger()

    # Instantiating the WS will make it connect. Be sure to add your api_key/api_secret.
    ws = BitMEXWebsocket(endpoint="https://testnet.bitmex.com/api/v1", symbol="XBTUSD",
                         api_key=None, api_secret=None)

    logger.info("Instrument data: %s" % ws.get_instrument())

    #"""
    # Run forever
    while ws.ws.sock.connected:
        logger.info("Ticker: %s" % ws.get_ticker())
        if ws.api_key:
            logger.info("Funds: %s" % ws.funds())
        logger.info("Market Depth: %s" % ws.market_depth())
        logger.info("Recent Trades: %s\n\n" % ws.recent_trades())
        # sleep(10)

        #Publishes multiple messages to a Pub/Sub topic.
        print("Publishing to cloud")
        for message in ws.market_depth():
            # Data must be a bytestring
            data = str(message).encode('utf-8')
            # When you publish a message, the client returns a future.
            print(data)
            publisher.publish(topic_path, data=data)
    #"""

"""
    # Timer
    import time
    start = time.time()
    print("Starting Timer:")
    i = 0
    for message in ws.market_depth():
        i = i + 1
        print(i)
        if i > 999:
            break
        # Data must be a bytestring
        data = str(message).encode('utf-8')
        # When you publish a message, the client returns a future.
        #print(data)
        publisher.publish(topic_path, data=data)
        #print(i)

    end = time.time()
    print(end - start)
"""

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
