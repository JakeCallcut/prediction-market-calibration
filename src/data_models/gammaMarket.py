class GammaMarket():

    def __init__(self, raw):
        self.raw = raw

    #Direct Properties

    @property
    def question(self):
        return self.raw.get("question")

    @property
    def outcomes(self):
        return self.raw.get("outcomes")

    @property
    def outcomePrices(self):
        return self.raw.get("outcomePrices")

    @property
    def resolved(self):
        return self.raw.get("umaResolutionStatus") == "resolved"

    @property
    def clobIds(self):
        return self.raw.get("clobTokenIds")

    # Derived Properties

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

