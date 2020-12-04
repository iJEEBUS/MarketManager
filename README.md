# MarketManager
<hr>

A class-based market management system that allows one api to be used to call multiple crypto-currency exchanges with one API call.
Any number of markets can be added to the system by simply filling in the code located in the `manager/MarketManager.py` class that each individual market inherits from -- for examples see either `markets/Coinbase.py` or `markets/Binance.py`.
