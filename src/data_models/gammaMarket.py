import json

class GammaMarket:

    def __init__(self, raw):
        self.raw = raw

    # Direct properties

    @property
    def question(self):
        return self.raw.get("question")

    @property
    def outcomes(self):
        return json.loads(self.raw.get("outcomes") or "[]")

    @property
    def outcomePrices(self):
        return [float(p) for p in json.loads(self.raw.get("outcomePrices") or "[]")]

    @property
    def resolved(self):
        return self.raw.get("umaResolutionStatus") == "resolved"

    @property
    def closedTime(self):
        return self.raw.get("closedTime")

    @property
    def clobIds(self):
        return json.loads(self.raw.get("clobTokenIds") or "[]")

    # Derived properties

    @property
    def winning_index(self):
        prices = self.outcomePrices
        if not prices:
            return None
        return prices.index(max(prices))

    @property
    def winning_outcome(self):
        i = self.winning_index
        outcomes = self.outcomes
        return outcomes[i] if i is not None and i < len(outcomes) else None

    @property
    def winning_token_id(self):
        i = self.winning_index
        tokens = self.clobIds
        return tokens[i] if i is not None and i < len(tokens) else None