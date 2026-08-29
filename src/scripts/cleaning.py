import pandas as pd
from pathlib import Path

DATA_PATH = Path("../../data/raw/market_data.csv")
MODELLING_TABLE_PATH = Path("../../data/processed/modelling_table.csv")

def clean_data():

    #Drop NA rows, scalar rows, and change yes/no to 0/1
    df = pd.read_csv(DATA_PATH)
    df = df.dropna()
    df = df.drop(df[df['outcome'] == "scalar"].index)
    df = df.replace({"outcome": {"yes": 0, "no": 1}})

    df.to_csv(MODELLING_TABLE_PATH, index=False)

if __name__ == "__main__":
    clean_data()