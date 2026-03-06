#STD
#TP
#LCL
from bt_engine.orders.fillOrder import _fillOrder
from bt_engine.orders.restOrder import _restOrder

def _placeOrder(engine, symbol, type, side, size, limit_price, stop_price, tp_points, sl_points):
    #Purpose of function: To send market, limit or stop orders to the engine.

    if symbol not in engine.market_data.keys():
        return
    
    timestamp = engine.timestamps[engine.current_row]
    symbol_close = engine.market_data[symbol]['c']
    current_symbol_close = symbol_close[engine.current_row]

    #Market Order
    if type == 1:
        _fillOrder(engine, symbol, timestamp, type, side, size, current_symbol_close, tp_points, sl_points)
        return

    #Limit Order
    elif type == 2:
        if limit_price is None:
            print('ORDER REJECTED: Limit orders must include a limit price.')
            return
        
        if side == 0:

            #Marketable buy limit order
            if limit_price > current_symbol_close:
                _fillOrder(engine, symbol, timestamp, type, side, size, current_symbol_close, tp_points, sl_points)
                return            
            #Resting buy limit order
            else:
                _restOrder(engine, symbol, timestamp, type, side, size, limit_price, tp_points, sl_points)
                return

        elif side == 1:
            #Marketable sell limit order
            if limit_price < current_symbol_close:
                _fillOrder(engine, symbol, timestamp, type, side, size, current_symbol_close, tp_points, sl_points)
                return
            #Resting sell limit order
            else:
                _restOrder(engine, symbol, timestamp, type, side, size, limit_price, tp_points, sl_points)
                return
    #Stop Order
    elif type == 3:
        if stop_price is None:
            print('ORDER REJECTED: Stop orders must include a stop price.')
            return

        if side == 0:
            #Invalid buy stop order
            if stop_price < current_symbol_close:
                print('ORDER REJECTED: For buy stop orders, stop price must be greater than current market price.')
                return
            #Resting buy stop order
            else:
                _restOrder(engine, symbol, timestamp, type, side, size, stop_price, tp_points, sl_points)
                return

        elif side == 1:
            #Invalid sell stop order
            if stop_price > current_symbol_close:
                print('ORDER REJECTED: For buy stop orders, stop price must be greater than current market price.')
                return
            #Resting sell stop order
            else:
                _restOrder(engine, symbol, timestamp, type, side, size, stop_price, tp_points, sl_points)
                return
    else:
        print('ORDER REJECTED: Order type not valid, must be 1 (Market order), 2 (Limit order), or 3 (Stop order).')
        return
