import os
from dotenv import load_dotenv
import asyncio
import pandas as pd
from datetime import datetime, timezone
import cybotrade_datasource
from backtest.backtest import Backtest
from backtest.strategy import SmaCrossStrategy, ExchangeFlowStrategy  # Assuming you have this class
from backtest.evaluation import evaluate_strategy

load_dotenv()

async def main():
    API_KEY = os.getenv("API_KEY")

    start = datetime(2024, 1, 1, tzinfo=timezone.utc)
    end = datetime(2025, 1, 1, tzinfo=timezone.utc)

    # === Fetch Data ===
    ohlcv_data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic='cryptoquant|btc/market-data/price-ohlcv?window=day',
        start_time=start,
        end_time=end
    )
    inflow_data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic='cryptoquant|btc/exchange-flows/inflow?exchange=binance&window=day',
        start_time=start,
        end_time=end
    )
    outflow_data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY,
        topic='cryptoquant|btc/exchange-flows/outflow?exchange=binance&window=day',
        start_time=start,
        end_time=end
    )

    # === Prepare DataFrames ===
    ohlcv_df = pd.DataFrame(ohlcv_data)
    inflow_df = pd.DataFrame(inflow_data)
    outflow_df = pd.DataFrame(outflow_data)

    outflow_df = outflow_df.rename(columns={
        'outflow_total': 'outflow_total',
        'outflow_top10': 'outflow_top10'
    })

    # Merge inflow and outflow
    flow_df = pd.merge(
        inflow_df,
        outflow_df,
        on=["start_time", "date"],
        how="outer",
        suffixes=('_inflow', '_outflow')
    )

    # Merge with OHLCV
    merged_df = pd.merge(
        flow_df,
        ohlcv_df,
        on=["start_time", "date"],
        how="inner"
    )

    # === SMA Strategy Backtest ===
    sma_windows = [5, 10, 20, 30, 50]
    sma_performance = pd.DataFrame(columns=["Sharpe Ratio", "Max Drawdown", "Trade per interval"], index=sma_windows)

    for window in sma_windows:
        bt = Backtest(data=ohlcv_df, strategy_class=SmaCrossStrategy, window=window)
        results = bt.run()
        metrics = evaluate_strategy(results)
        sma_performance.loc[window] = metrics

    print("\n=== SMA Strategy Performance ===")
    print(sma_performance)

    # === Exchange Flow Strategy Backtest ===
    thresholds = [100, 500, 1000, 2000]
    flow_performance = pd.DataFrame(columns=["Sharpe Ratio", "Max Drawdown", "Trade per interval"], index=thresholds)

    for t in thresholds:
        strategy = ExchangeFlowStrategy(merged_df, threshold=t)
        results = strategy.run()
        metrics = evaluate_strategy(results)
        flow_performance.loc[t] = metrics

    print("\n=== Exchange Flow Strategy Performance ===")
    print(flow_performance)

if __name__ == "__main__":
    asyncio.run(main())
