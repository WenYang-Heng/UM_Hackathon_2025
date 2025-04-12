import numpy as np
import pandas as pd

def calculate_sharpe_ratio(df):
    pnl = df['pnl'].dropna()
    return (pnl.mean() / pnl.std() * np.sqrt(365))

def calculate_max_drawdown(df):
    return df['drawdown'].min()

def calculate_trade_per_interval(df):
    return df['trade'].sum() / len(df)

def evaluate_strategy(df):
    return {
        "Sharpe Ratio": calculate_sharpe_ratio(df),
        "Max Drawdown": calculate_max_drawdown(df),
        "Trade per interval": calculate_trade_per_interval(df)
    }
