import os
from dotenv import load_dotenv
import asyncio
import pandas as pd
import cybotrade_datasource
from datetime import datetime, timezone
from backtest.backtest import Backtest
from backtest.strategy import SmaCrossStrategy
from backtest.evaluation import evaluate_strategy

load_dotenv()

async def main():
    API_KEY = os.getenv("API_KEY")
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic='cryptoquant|btc/market-data/price-ohlcv?window=day', 
        # topic='cryptoquant|btc/exchange-flows/netflow?exchange=binance&window=day&limit=2', 
        # above topic is just for testing
        # topic format must follow above, the endpoint need to refer to the respective document, endpoint is after |
        start_time=datetime(year=2024, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    print(df)

    windows = [5, 10, 20, 30, 50]
    performance = pd.DataFrame(columns=["Sharpe Ratio", "Max Drawdown", "Trade per interval"], index=windows)

    for window in windows:
        bt = Backtest(
            data=df,
            strategy_class=SmaCrossStrategy,
            window=window
        )

        results = bt.run() 
        print(results)
        metrics = evaluate_strategy(results)

        performance.loc[window] = metrics

    # Show performance table
    print(performance)

asyncio.run(main())