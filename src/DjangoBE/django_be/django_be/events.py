import uuid
from datetime import datetime

def make_event(event_type: str, payload: dict) -> dict:
    return {
        'id': str(uuid.uuid4()),
        'type': event_type,
        'timestamp': datetime.utcnow().isoformat(),
        'payload': payload,
    }

def order_placed(order_id, user_id, side, amount, price):
    return make_event('OrderPlaced', {
        'order_id': order_id,
        'user_id': user_id,
        'side': side,
        'amount': amount,
        'price': price,
    })

def order_cancelled(order_id, user_id):
    return make_event('OrderCancelled', {'order_id': order_id, 'user_id': user_id})

def trade_executed(trade_id, buy_order_id, sell_order_id, amount, price):
    return make_event('TradeExecuted', {
        'trade_id': trade_id,
        'buy_order_id': buy_order_id,
        'sell_order_id': sell_order_id,
        'amount': amount,
        'price': price,
    })

def funds_debited(user_id, amount):
    return make_event('FundsDebited', {'user_id': user_id, 'amount': amount})

def funds_credited(user_id, amount):
    return make_event('FundsCredited', {'user_id': user_id, 'amount': amount})