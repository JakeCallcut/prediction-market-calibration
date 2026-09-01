from src import config
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

SOURCES = ["polymarket", "kalshi"]
COLORS = {"polymarket": "#5B4FC7", "kalshi": "#1D9E75"}
LABELS = {"polymarket": "Polymarket", "kalshi": "Kalshi"}


def calc_reliability(df, horizon, n_bins=10):
    d = df[df["horizon"] == horizon]
    bins = np.linspace(0, 1, n_bins + 1)
    d = d.assign(bin=np.clip(np.digitize(d["forecast"], bins) - 1, 0, n_bins - 1))
    g = d.groupby("bin").agg(mean_forecast=("forecast", "mean"),
                             obs_freq=("outcome", "mean"),
                             n=("outcome", "size"))
    return g


def _wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    denom = 1 + z**2 / n
    centre = (p + z**2 / (2 * n)) / denom
    half = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return centre - half, centre + half


def plot_calibration(df, n_bins=10, save_path=None):
    plt.rcParams.update({"font.size": 12, "axes.edgecolor": "#888780",
                         "axes.linewidth": 0.8, "figure.facecolor": "white",
                         "axes.facecolor": "white"})
    fig, axes = plt.subplots(2, 4, figsize=(22, 11), sharex=True, sharey=True)
    fig.suptitle("Market calibration by source and forecast horizon",
                 fontsize=22, y=0.98)

    for r, source in enumerate(SOURCES):
        color = COLORS[source]
        src_df = df[df["source"] == source]
        for c, horizon in enumerate(config.HORIZONS.keys()):
            ax = axes[r, c]
            ax.plot([0, 1], [0, 1], ls="--", lw=1.2, color="#B4B2A9", zorder=1)

            sub = src_df[src_df["horizon"] == horizon]
            g = calc_reliability(src_df, horizon, n_bins) if len(sub) else None

            if g is None or g.empty:
                ax.text(0.5, 0.5, "no data", ha="center", va="center",
                        color="#B4B2A9", fontsize=14)
            else:
                mf, of, ns = g["mean_forecast"].to_numpy(), g["obs_freq"].to_numpy(), g["n"].to_numpy()
                ci = [_wilson(int(round(o * n)), int(n)) for o, n in zip(of, ns)]
                lo = np.array([a for a, _ in ci])
                hi = np.array([b for _, b in ci])

                ax.fill_between(mf, mf, of, color=color, alpha=0.10, zorder=2)
                ax.vlines(mf, lo, hi, color=color, alpha=0.45, lw=1.4, zorder=3)
                ax.plot(mf, of, color=color, lw=1.6, alpha=0.7, zorder=4)
                ax.scatter(mf, of, s=30 + np.sqrt(ns) * 22, color=color,
                           edgecolor="white", linewidth=1.2, zorder=5)

                brier = float(np.mean((sub["forecast"] - sub["outcome"]) ** 2))
                ax.text(0.04, 0.93, f"Brier {brier:.3f}\nN = {len(sub):,}",
                        transform=ax.transAxes, va="top", fontsize=11, color="#444441")

            ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.set_aspect("equal")
            ax.set_xticks([0, .25, .5, .75, 1]); ax.set_yticks([0, .25, .5, .75, 1])
            ax.grid(True, color="#F1EFE8", lw=0.8, zorder=0)
            for s in ("top", "right"):
                ax.spines[s].set_visible(False)
            if r == 0:
                ax.set_title(horizon, fontsize=15, pad=10)
            if c == 0:
                ax.set_ylabel(f"{LABELS[source]}\n\nobserved frequency", fontsize=13)
            if r == 1:
                ax.set_xlabel("mean forecast", fontsize=12)

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    if save_path:
        fig.savefig(save_path, dpi=200, bbox_inches="tight")
    return fig