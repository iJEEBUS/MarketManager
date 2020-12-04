import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from websocket import create_connection
from CONFIG import COINBASE_NAME, COINBASE_KEY, COINBASE_SECRET, COINBASE_PASS, COINBASE_API_URL, COINBASE_WS_URL
from Market import Market

class Coinbase(Market):
    
    def __init__(self):
        super(Coinbase, self).__init__(COINBASE_KEY, COINBASE_SECRET, COINBASE_PASS, COINBASE_API_URL, COINBASE_WS_URL, "Coinbase")
    
    def connectToWebsocket(self, product_ids=[ "ETH-USD"], channels=["heartbeat", "ticker"]):
        # Connect and send message to websocket server
        self.ws = create_connection(self.ws_url)
        msg = json.dumps({"type": "subscribe","product_ids": product_ids,"channels": channels}, indent=4)
        self.ws.send(msg)
        print("Now connected to %s", self.ws_url)
        
    def getCurrentPrices(self):
        """Return current bid/ask/price tuple"""
        # add one more request as the first is a connection message
        for i in range(2):
            res = json.loads(self.ws.recv())
            if i > 0:
                try:
                    return (res['best_bid'], res['best_ask'])
                except KeyError as e:
                    return (None, None)