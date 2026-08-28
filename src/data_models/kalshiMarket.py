
class KalshiMarket:
    """Data model for a Kalshi market"""
    def __init__(self, raw):
        self.raw = raw

    #tag for a particular market
    @property
    def ticker(self):
        return self.raw.get("ticker")

    #category of market, derivable from its ticker
    @property
    def series(self):
        return self.ticker.split("-")[0]

    #the question being asked in the market
    @property
    def title(self):
        return self.raw.get("title")

    #the resolved outcome of the market
    @property
    def result(self):
        return self.raw.get("result") or None

    #the datetime which the market resolved
    @property
    def closedTime(self):
        return self.raw.get("close_time")