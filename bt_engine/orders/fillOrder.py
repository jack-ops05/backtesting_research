#STD
#TP
import uuid
#LCL

def _fillOrder(engine, symbol, timestamp, type, side, size, fill_price, tp_points, sl_points):
    #Purpose of function: To fill any orders requested and open positions.

    #Calculate tp/sl
    if tp_points != None:
        if side == 0:
            tp = fill_price + tp_points
        elif side == 1:
            tp = fill_price - tp_points
    if sl_points != None:
        if side == 0:
            sl = fill_price - sl_points
        elif side == 1:
            sl = fill_price + sl_points
    if tp_points == None:
        tp = None
    if sl_points == None:
        sl = None

    filled_order = {
        'order_id': uuid.uuid4(),
        'timestamp': timestamp,
        'symbol': symbol,
        'type': type,
        'side': side,
        'size': size,
        'fill_price': fill_price,
        'tp': tp,
        'sl': sl
    }
    engine.filled_orders.append(filled_order)

    position = {
        'position_id': uuid.uuid4(),
        'symbol': symbol,
        'side': side,
        'size': size,
        'entry_price': fill_price,
        'entry_timestamp': engine.timestamps[engine.current_row],
        'entry_bar': engine.current_row,
        'tp': tp,
        'sl': sl
    }
    engine.positions.append(position)
