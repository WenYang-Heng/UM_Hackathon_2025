## Project Presentation
You can view our presentation slides [here](https://www.canva.com/design/DAGkZ5qtnas/rq_EqoortXMd-4HMSf6bQw/edit?utm_content=DAGkZ5qtnas&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton).

## Prerequisites

Ensure that **Python 3.11** or **3.12** is installed as the project uses [`cybotrade-datasource`](https://pypi.org/project/cybotrade-datasource/) which currently support these versions.

You can verify your Python version by running:

```bash
python --version
```

## Introduction

This project is a lightweight backtesting library focused on evaluating trading strategies using historical cryptocurrency data. It currently implements a **Simple Moving Average (SMA)** crossover strategy.

The backtest pulls **Bitcoin (BTC)** market data from **CryptoQuant** from **2024-01-01 to 2025-01-01**. The strategy calculates metrics such as equity, drawdown, and Sharpe ratio to assess performance over time.


