class Account:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 0.0
        self.shares = {}

    def apply(self, event: dict):
        t = event['type']
        p = event['payload']

        if t == 'FundsDebited' and p['user_id'] == self.user_id:
            self.balance -= p['amount']

        elif t == 'FundsCredited' and p['user_id'] == self.user_id:
            self.balance += p['amount']
        elif t == 'SharesDebited' and p['user_id'] == self.user_id:
            stock = p['stock']
            amt = p['amount']
            self.shares[stock] = self.shares.get(stock, 0) - amt
        elif t == 'SharesCredited' and p['user_id'] == self.user_id:
            stock = p['stock']
            amt = p['amount']
            self.shares[stock] = self.shares.get(stock, 0) + amt
        elif t == 'TradeExecuted':
            if p['buy_user_id'] == self.user_id:
                self.shares[p['stock']] = self.shares.get(p['stock'], 0) + p['amount']
            if p['sell_user_id'] == self.user_id:
                self.shares[p['stock']] = self.shares.get(p['stock'], 0) - p['amount']
            if p['buy_user_id'] == self.user_id:
                self.balance -= p['amount'] * p['price']
            if p['sell_user_id'] == self.user_id:
                self.balance += p['amount'] * p['price']

    def replay(self, events: list):
        for e in events:
            self.apply(e)
        return self
