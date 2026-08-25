import json

class KalshiMarket:

    def __init__(self, raw):
        self.raw = raw

    @property
    def title(self):
        return self.raw.get("title")

    @property
    def result(self):
        return self.raw.get("result") or None

    @property
    def closedTime(self):
        return self.raw.get("close_time")