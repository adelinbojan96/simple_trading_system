import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .event_store import append_event, get_all_events
from .events import *
from .aggregates.order_book import *
from .aggregates.account import *

@csrf_exempt
def place_order(request):
    try:
        data     = json.loads(request.body)
        user     = data['user_id']
        side     = data['side']
        price    = data['price']
        stock    = data['stock']
        currency = data['currency']

        order_id = str(uuid.uuid4())

        events     = get_all_events()
        ob         = OrderBook().replay(events)

        buyer_acct = Account(user).replay(get_all_events())
        if side == 'buy' and buyer_acct.balance < price:
            return JsonResponse({'error': 'Insufficient funds for trade'}, status=400)

        append_event(order_placed(order_id, user, side, price, stock, currency))

        # match one share
        counter = ob.sell if side=='buy' else ob.buy
        for co_id, co in counter.items():
            if co['stock'] == stock and co['price'] == price and co['currency'] == currency:

                print(f"Matched: {order_id} with {co_id}")

                trade_id = str(uuid.uuid4())
                buy_id   = order_id if side=='buy'  else co_id
                sell_id  = co_id     if side=='buy'  else order_id
                buy_user = user      if side=='buy'  else co['user_id']
                sell_user= co['user_id'] if side=='buy' else user

                # update amounts
                append_event(funds_debited(buy_user,  price))
                append_event(funds_credited(sell_user, price))

                # delete the matching orders and append the trade event
                append_event(trade_executed(
                    trade_id, buy_id, sell_id,
                    buy_user, sell_user,
                    price,
                    stock,
                    currency
                ))

                buyer_acct = Account(buy_user).replay(get_all_events())
                seller_acct = Account(sell_user).replay(get_all_events())
                print(f"{buy_user} balance:   {buyer_acct.balance}{currency}")
                print(f"{sell_user} balance:  {seller_acct.balance}{currency}")
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