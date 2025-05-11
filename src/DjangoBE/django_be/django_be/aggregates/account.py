class Account:
    def __init__(self, user_id):
        self.user_id = user_id
        self.balance = 5000.0
        self.shares = {}

    def apply(self, event: dict):
        t = event['type']
        p = event['payload']

        if t == 'FundsDebited' and p['user_id'] == self.user_id:
            self.balance -= p['amount']

        elif t == 'FundsCredited' and p['user_id'] == self.user_id:
            self.balance += p['amount']

    def replay(self, events: list):
        for e in events:
            self.apply(e)
        return self
