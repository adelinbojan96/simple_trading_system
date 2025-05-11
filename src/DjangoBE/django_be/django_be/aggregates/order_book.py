class OrderBook:
    def __init__(self):
        self.buy = {}
        self.sell = {}
        self.trades = []
        self.cancelled = []
    def apply(self, event):
        t, p = event['type'], event['payload']

        if t == 'OrderPlaced':
            if p['side'] == 'buy':
                self.buy[p['order_id']] = dict(p)
            else:
                self.sell[p['order_id']] = dict(p)

        elif t == 'OrderCancelled':
            if p['order_id'] in self.buy:
                del self.buy[p['order_id']]
            elif p['order_id'] in self.sell:
                del self.sell[p['order_id']]
            self.cancelled.append(p['order_id'])

        elif t == 'TradeExecuted':
            self.trades.append(dict(p))
            if p['buy_order_id'] in self.buy:
                del self.buy[p['buy_order_id']]
            if p['sell_order_id'] in self.sell:
                del self.sell[p['sell_order_id']]

    def replay(self, events):
        for e in events:
            self.apply(e)
        return self
