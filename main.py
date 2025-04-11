import asyncio
import pandas as pd
import cybotrade_datasource
from datetime import datetime, timezone
API_KEY = "hWHSN90KeaFig5qpHxqS1UyI7Z2PpyUcwZso2CoyV4woGLrM"

async def main():
    data = await cybotrade_datasource.query_paginated(
        api_key=API_KEY, 
        topic='cryptoquant|btc/market-data/price-ohlcv?window=day', 
        # above topic is just for testing
        # topic format must follow above, the endpoint need to refer to the respective document, endpoint is after |
        start_time=datetime(year=2024, month=1, day=1, tzinfo=timezone.utc),
        end_time=datetime(year=2025, month=1, day=1, tzinfo=timezone.utc)
    )
    df = pd.DataFrame(data)
    print(df)

asyncio.run(main())