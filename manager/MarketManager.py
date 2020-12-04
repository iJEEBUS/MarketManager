# One class that will handle all of the interactions between the exchanges
class MarketManager(object):
    def __init__(self):

        # Create controllers
        self.controllers = [Coinbase(), Binance()]
        self.threads = []

    def run(self):
        """Runs the entire program"""
        # Connect to websockets
        self.connectToWebsockets()

        while True:
            time.sleep(1)
            self.checkForTradeOpportunity()

    def stop(self):
        """Wrapper to stop the program gracefully"""
        self.disconnectFromWebsockets()

    def connectToWebsockets(self):
        self.threads = [threading.Thread(target=c.connectToWebsocket, args=()) for c in self.controllers]

        # Start threads
        [t.start() for t in self.threads]

        # Wait for them to finish running before proceeding
        [t.join() for t in self.threads]


    def disconnectFromWebsockets(self):
        self.threads = [threading.Thread(target=c.disconnect, args=()) for c in self.controllers]

        # Start threads
        [t.start() for t in self.threads]

        # Wait for them to finish running before proceeding
        [t.join() for t in self.threads]

    def displayPrices(self):
        self.threads = [threading.Thread(target=c.showStream, args=()) for c in self.controllers]

        # Start threads
        [t.start() for t in self.threads]

        # Wait for them to finish running before proceeding
        [t.join() for t in self.threads]


    def calculateBidAskDeltas(self):
        all_bids = []
        all_asks = []

        for c in self.controllers:
            bid, ask = c.getCurrentPrices()
            if None in [bid, ask]:
                return (None, None)
            else:
                all_bids.append(float(bid))
                all_asks.append(float(ask))

        # Check if the bid on one exchange is higher than the ask on another
        c_bid_minus_b_ask = all_bids[0] - all_asks[-1] # coinbase bid - binance ask
        b_bid_minus_c_ask = all_bids[-1] - all_asks[0] # binance bid - coinbase ask

        deltas = tuple([c_bid_minus_b_ask, b_bid_minus_c_ask])

        return deltas

    def checkForTradeOpportunity(self):

        deltas = self.calculateBidAskDeltas()
        if None in deltas:
            return

        buy_coinbase = False
        buy_binance = False

        if abs(deltas[0]) > abs(deltas[-1]):
            # (coinbase bid - binance ask) > (binance bid - coinbase ask)

            if deltas[0] > 0.0:
                buy_coinbase = False
                buy_binance = True
            else:
                buy_coinbase = True
                buy_binance = False

        elif abs(deltas[0]) < abs(deltas[-1]):

            if deltas[-1] > 0.0:
                buy_coinbase = True
                buy_binance = False
            else:
                buy_coinbase = False
                buy_binance = True

        print(deltas, (buy_coinbase, buy_binance))