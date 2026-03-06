#STD
#TP
import uuid
#LCL

def _restOrder(engine, symbol, timestamp, type, side, size, rest_price, tp_points, sl_points):
    #Purpose of function: To send resting limit or stop orders to the engine.

    resting_order = {
        'order_id': uuid.uuid4,
        'timestamp': timestamp,
        'symbol': symbol,
        'type': type,
        'side': side,
        'size': size,
        'rest_price': rest_price,
        'tp_points': tp_points,
        'sl_points': sl_points
    }
    engine.resting_orders.append(resting_order)
