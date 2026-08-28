import json

class GammaMarket:
    """Data model for a Polymarket Market, as parsed from the Gamma API"""
    def __init__(self, raw):
        self.raw = raw

    # Direct properties

    #the question being asked in the market
    @property
    def question(self):
        return self.raw.get("question")

    #list of possible outcomes
    @property
    def outcomes(self):
        return json.loads(self.raw.get("outcomes") or "[]")

    #list of prices associated with each outcome
    @property
    def outcomePrices(self):
        return [float(p) for p in json.loads(self.raw.get("outcomePrices") or "[]")]

    #boolean indicating whether the market resolved
    @property
    def resolved(self):
        return self.raw.get("umaResolutionStatus") == "resolved"

    #the datetime at which the market resolved
    @property
    def closedTime(self):
        return self.raw.get("closedTime")

    #list of IDs for the different outcomes, to be passed to the CLOB API for further price info
    @property
    def clobIds(self):
        return json.loads(self.raw.get("clobTokenIds") or "[]")

    # Derived properties

    #index in the list of outcomes which resolved true
    @property
    def winning_index(self):
        prices = self.outcomePrices
        if not prices:
            return None
        return prices.index(max(prices))

    #the outcome which resolved true
    @property
    def winning_outcome(self):
        i = self.winning_index
        outcomes = self.outcomes
        return outcomes[i] if i is not None and i < len(outcomes) else None

    #the CLOB ID of the outcome which resolved true
    @property
    def winning_token_id(self):
        i = self.winning_index
        tokens = self.clobIds
        return tokens[i] if i is not None and i < len(tokens) else None