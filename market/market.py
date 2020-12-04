import json, hmac, hashlib, time, requests, base64
from requests.auth import AuthBase
from websocket import create_connection

class Market(AuthBase):

    def __init__(self, api_key, secret_key, passphrase, api_url, ws_url, name):
        self.api_key = api_key
        self.secret_key = secret_key
        self.passphrase = passphrase
        self.api_url = api_url
        self.ws_url = ws_url
        self.name = name
        self.ws = None

    def __call__(self, request):
        timestamp = str(time.time())
        message = timestamp + request.method + request.path_url + (request.body or '')
        hmac_key = base64.b64decode(self.secret_key)
        signature = hmac.new(hmac_key, message, hashlib.sha256)
        signature_b64 = signature.digest().encode('base64').rstrip('\n')

        request.headers.update({
            'CB-ACCESS-SIGN': signature_b64,
            'CB-ACCESS-TIMESTAMP': timestamp,
            'CB-ACCESS-KEY': self.api_key,
            'CB-ACCESS-PASSPHRASE': self.passphrase,
            'Content-Type': 'application/json'
        })
        return request
    
    def connectToWebsocket(self):
        """Subscribe to a websocket"""
        pass

    def showStream(self, N=2):
        for _ in range(N):
            temp = self.ws.recv()
            print(temp)

        
    def disconnect(self):
        """Close all websocket connections"""
        print("Closing connection to %s", self.ws_url)
        self.ws.close()
        
    def getCurrentPrices(self):
        """Returns the best bid and ask prices as a tuple"""
        pass