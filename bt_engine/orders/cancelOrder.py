#STD
#TP
#LCL

def _cancelOrder(engine, order_id):
    #Purpose of function: Allows user to cancel resting orders via order id.
    order_to_cancel = None
    for order in engine.resting_orders:
        if order['order_id'] == order_id:
            order_to_cancel = order
            break
        else:
            continue
    if order_to_cancel == None:
        print('ERROR: Failed to cancel order, order id not found.')
        return
    else:
        engine.resting_orders.remove(order_to_cancel)
