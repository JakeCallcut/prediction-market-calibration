#Simple script to clean the raw market data and save to a modelling table
#run as main to clean

from src import config
import pandas as pd

def clean_data():
    """cleant the data at the raw path in config, save the modlling table and platform split tables"""

    #Drop NA rows, scalar rows, and change yes/no to 0/1
    df = pd.read_csv(config.RAW_DATA_PATH / "market_data.csv")
    df = df.dropna()
    df = df.drop(df[df['outcome'] == "scalar"].index)
    df = df.replace({"outcome": {"yes": 1, "no": 0}})

    #split dataframe by source platform
    df_polymarket = df[df['source'] == 'polymarket']
    df_kalshi = df[df['source'] == 'kalshi']

    #save all dataframes
    df.to_csv(config.PROC_DATA_PATH / "modelling_table.csv", index=False)
    df_polymarket.to_csv(config.PROC_DATA_PATH / "polymarket_table.csv", index=False)
    df_kalshi.to_csv(config.PROC_DATA_PATH / "kalshi_table.csv", index=False)

    return df

if __name__ == "__main__":
    clean_data()