from collect.clob import price_at
from collect.gamma import FetchMarkets

def fetchData():
    gamma_markets = FetchMarkets(100)
    for m in gamma_markets:
        print(m.question, m.outcomes, "->", m.winning_outcome, "resolved:", m.resolved, "ClobId: ", m.clobIds[0])
        m_clob_id = m.clobIds[0]

if __name__ == "__main__":
    fetchData()