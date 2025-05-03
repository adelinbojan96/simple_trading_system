import json, uuid
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from event_store import EventStore
from events import *
from aggregates.order_book import OrderBook
from aggregates.account import Account

@csrf_exempt
def place_order(request):
    d = json.loads(request.body)
    oid = str(uuid.uuid4())
    if d['side']=='buy':
        EventStore.append(FundsDebited(d['user_id'], d['amount']*d['price']))
    EventStore.append(OrderPlaced(oid, d['user_id'], d['side'], d['amount'], d['price']))
    return JsonResponse({'order_id': oid})

@csrf_exempt
def cancel_order(request):
    d = json.loads(request.body)
    EventStore.append(OrderCancelled(d['order_id'], d['user_id']))
    return JsonResponse({'status':'cancelled'})

@csrf_exempt
def replay_state(request):
    ev = EventStore.get_all_events()
    ob = OrderBook().replay(ev)
    uid = request.GET.get('user_id')
    acct = Account(uid).replay(ev) if uid else None
    return JsonResponse({
        'buy': list(ob.buy.values()),
        'sell': list(ob.sell.values()),
        'trades': ob.trades,
        'balance': acct.balance if acct else None,
    })