# evaluation.py

import numpy as np
import pandas as pd

def calculate_sharpe_ratio(df):
    pnl = df['pnl'].dropna()
    return (pnl.mean() / pnl.std() * np.sqrt(365))

def calculate_max_drawdown(df):
    return df['drawdown'].min()

def calculate_trade_per_interval(df):
    return df['trade'].sum() / len(df)

# def calculate_cagr(df, periods_per_year=252):
#     """
#     Calculate CAGR using 'equity' column.
#     """
#     equity = df['equity']
#     start_value = equity.iloc[0]
#     end_value = equity.iloc[-1]
#     n_periods = len(equity)
#     years = n_periods / periods_per_year
#     if years <= 0 or start_value == 0:
#         return 0
#     return (end_value / start_value) ** (1 / years) - 1

def evaluate_strategy(df):
    """
    Accepts the result DataFrame of a strategy and returns evaluation metrics.
    """
    return {
        "Sharpe Ratio": calculate_sharpe_ratio(df),
        "Max Drawdown": calculate_max_drawdown(df),
        "Trade per interval": calculate_trade_per_interval(df)
    }
