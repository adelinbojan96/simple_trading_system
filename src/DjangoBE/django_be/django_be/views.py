import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .event_store import append_event, get_all_events
from .events import *
from .aggregates.order_book import *
from .aggregates.account import Account

@csrf_exempt
def place_order(request):
    try:
        data     = json.loads(request.body)
        user     = data['user_id']
        side     = data['side']
        price    = data['price']
        stock    = data['stock']
        order_id = str(uuid.uuid4())

        events     = get_all_events()
        ob         = OrderBook().replay(events)

        append_event(order_placed(order_id, user, side, price, stock))

        # match one share
        counter = ob.sell if side=='buy' else ob.buy
        for co_id, co in counter.items():
            if co['stock']==stock and co['price']==price:

                print(f"Matched: {order_id} with {co_id}")
                # delete the matching orders
                append_event(order_cancelled(order_id, user))
                append_event(order_cancelled(co_id, co['user_id']))

                trade_id = str(uuid.uuid4())
                buy_id   = order_id if side=='buy'  else co_id
                sell_id  = co_id     if side=='buy'  else order_id
                buy_user = user      if side=='buy'  else co['user_id']
                sell_user= co['user_id'] if side=='buy' else user

                append_event(trade_executed(
                    trade_id, buy_id, sell_id,
                    buy_user, sell_user,
                    price,
                    stock,
                ))

                append_event(funds_debited(buy_user,  price))
                append_event(funds_credited(sell_user, price))
                append_event(shares_debited(sell_user, stock, 1))
                append_event(shares_credited(buy_user,  stock, 1))
                break


        return JsonResponse({'status':'ok','order_id':order_id})

    except Exception as e:
        return JsonResponse({'error':str(e)},status=400)

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
    events = get_all_events()
    ob     = OrderBook().replay(events)

    return JsonResponse({
        'buy':       ob.buy,
        'sell':      ob.sell,
        'cancelled': ob.cancelled,
        'trades':    ob.trades,
    })