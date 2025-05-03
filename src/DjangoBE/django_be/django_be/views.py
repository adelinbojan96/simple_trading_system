import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .event_store import append_event, get_all_events
from .events import *
from .aggregates.order_book import OrderBook
from .aggregates.account import Account

@csrf_exempt
def place_order(request):
    try:
        data = json.loads(request.body)
        user_id = data['user_id']
        side = data['side']
        amount = data['amount']
        price = data['price']
        stock = data.get('stock')
        currency = data.get('currency')
        order_id = str(uuid.uuid4())

        # Debit funds on buy
        if side == 'buy':
            append_event(funds_debited(user_id, amount * price))
        # Create order event
        evt = order_placed(order_id, user_id, side, amount, price, stock)
        if currency:
            evt['payload']['currency'] = currency
        append_event(evt)

        return JsonResponse({'status': 'ok', 'order_id': order_id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def cancel_order(request):
    try:
        data = json.loads(request.body)
        append_event(order_cancelled(data['order_id'], data['user_id']))
        return JsonResponse({'status': 'cancelled'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def replay_state(request):
    try:
        events = get_all_events()
        ob = OrderBook().replay(events)
        user_id = request.GET.get('user_id')
        acct = Account(user_id).replay(events) if user_id else None

        return JsonResponse({
            'buy': ob.buy,
            'sell': ob.sell,
            'trades': ob.trades,
            'balance': acct.balance if acct else None
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)