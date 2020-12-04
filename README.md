# MarketManager
A class-based market management system that allows a single API call to send the same command to multiple crypto-currency exchanges at once.

Any number of markets can be added to the system by simply filling in the code located in the `manager/MarketManager.py` class that each individual market inherits from -- for examples see either `markets/Coinbase.py` or `markets/Binance.py`.
