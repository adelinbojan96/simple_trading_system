class Account:
    def __init__(self, user_id):
        self.user_id, self.balance = user_id, 0.0

    def apply(self, event):
        t, p = event['type'], event['payload']
        if p.get('user_id') != self.user_id: return
        if t == 'FundsDebited':   self.balance -= p['amount']
        elif t == 'FundsCredited': self.balance += p['amount']

    def replay(self, events):
        for e in events: self.apply(e)
        return self