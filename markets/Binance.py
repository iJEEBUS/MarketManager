import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from websocket import create_connection
from CONFIG import BINANCE_KEY, BINANCE_SECRET, BINANCE_PASS, BINANCE_API_URL, BINANCE_WS_URL

class Binance(Market):

    def __init__(self):
        super(Binance, self).__init__(BINANCE_KEY, BINANCE_SECRET, BINANCE_PASS, BINANCE_API_URL, BINANCE_WS_URL, "Binance")

    
    def connectToWebsocket(self):
        # Connect and send message to websocket server
        print(self.ws_url)
        self.ws = create_connection(self.ws_url)
        msg = json.dumps({"method": "SUBSCRIBE", "params": ["ethusdt@bookTicker"], "id": 312}, indent=4)
        self.ws.send(msg)
        print("Now connected to %s", self.ws_url)
        
    def getCurrentPrices(self):
        """Return current bid/ask/price tuple"""
        # add one more request as the first is a connection message
        for i in range(2):
            res = json.loads(self.ws.recv())
            if i > 0:
                try:
                    return (res['b'], res['a'])
                except KeyError as e:
                    return (None, None)