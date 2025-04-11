class Broker:
    def __init__(self, cash=100000, commission=0.001):
        self.cash = cash
        self.positions = {}  # e.g., {'BTC': {'quantity': 1.0, 'avg_price': 25000}}
        self.commission = commission
        self.equity_curve = []

    def place_order(self, asset, quantity, price):
        cost = quantity * price
        fee = cost * self.commission

        if quantity > 0:  # Buy
            total_cost = cost + fee
            if self.cash >= total_cost:
                self.cash -= total_cost
                self._update_position(asset, quantity, price)
        elif quantity < 0:  # Sell
            self._sell_position(asset, abs(quantity), price, fee)

    def _update_position(self, asset, quantity, price):
        if asset not in self.positions:
            self.positions[asset] = {'quantity': 0, 'avg_price': 0}
        pos = self.positions[asset]
        total_qty = pos['quantity'] + quantity
        pos['avg_price'] = (pos['quantity'] * pos['avg_price'] + quantity * price) / total_qty
        pos['quantity'] = total_qty

    def _sell_position(self, asset, quantity, price, fee):
        if asset in self.positions and self.positions[asset]['quantity'] >= quantity:
            proceeds = quantity * price - fee
            self.cash += proceeds
            self.positions[asset]['quantity'] -= quantity
            if self.positions[asset]['quantity'] == 0:
                del self.positions[asset]

    def get_equity(self, current_price_lookup=None):
        equity = self.cash
        for asset, pos in self.positions.items():
            if current_price_lookup:
                current_price = current_price_lookup(asset)
            else:
                current_price = pos['avg_price']
            equity += pos['quantity'] * current_price
        return equity
