class OrderBook:
    def __init__(self):
        self.buy = {}
        self.sell = {}
        self.trades = []

    def apply(self, event):
        t, p = event['type'], event['payload']
        if t == 'OrderPlaced':
            (self.buy if p['side']=='buy' else self.sell)[p['order_id']] = p
        elif t == 'OrderCancelled':
            self.buy.pop(p['order_id'], None)
            self.sell.pop(p['order_id'], None)
        elif t == 'TradeExecuted':
            self.trades.append(p)

    def replay(self, events):
        for e in events: self.apply(e)
        return self
