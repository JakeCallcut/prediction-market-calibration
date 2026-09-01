from scripts.calibration import plot_calibration
from src.scripts.fetch_data import fetch_data
from src.scripts.cleaning import clean_data
from src import config
import matplotlib.pyplot as plt
import pandas as pd

def main():
    fetch_data(config.NUM_MARKETS)
    clean_data()

    df = pd.read_csv(config.PROC_DATA_PATH / "modelling_table.csv")
    kalshi_df = pd.read_csv(config.PROC_DATA_PATH / "kalshi_table.csv")
    poly_df = pd.read_csv(config.PROC_DATA_PATH / "polymarket_table.csv")

    plot_calibration(df, save_path=config.RESULTS_PATH / "calibration.png")
    plt.show()

if __name__ == "__main__":
    main()