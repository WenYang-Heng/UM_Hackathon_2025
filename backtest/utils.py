def calculate_price_change(i, data):
    if i > 0:
        prev_price = data.iloc[i - 1]['close']
        current_price = data.iloc[i]['close']
        return (current_price - prev_price) / prev_price
    return 0

def calculate_trade_actions(prev_signal, current_signal):
    if current_signal != prev_signal:
        return 2 if abs(current_signal - prev_signal) == 2 else 1
    return 0

def calculate_drawdown(current_equity, history):
    if history and len(history) > 0:
        max_equity = max(h['equity'] for h in history)
    else:
        max_equity = current_equity
    return current_equity - max_equity

def calculate_pnl(price_change, prev_signal, trade_actions, fees):
    pnl = price_change * prev_signal
    fees = trade_actions * fees
    return pnl - fees