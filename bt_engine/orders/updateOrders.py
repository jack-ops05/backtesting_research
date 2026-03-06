#STD
#TP
#LCL
from bt_engine.orders.fillOrder import _fillOrder

def _updateOrders(engine):
    #Purpose of function: To check if resting orders have hit their specified resting prices, if condition is hit, orders will be filled at that resting price.

    if len(engine.resting_orders) > 0:
        for order in engine.resting_orders.copy():

            #Order lookups
            order_symbol = order['symbol']
            order_timestamp = order['timestamp']
            order_type = order['type']
            order_side = order['side']
            order_size = order['size']
            order_rest_price = order['rest_price']
            order_tp_points = order['tp_points']
            order_sl_points = order['sl_points']

            #Symbol lookups
            symbol_data = engine.market_data[order_symbol]
            symbol_current_high = symbol_data['h'][engine.current_row]
            symbol_current_low = symbol_data['l'][engine.current_row]

            #Limit order
            if order_type == 2:
                limit_price = order_rest_price

                if order_side == 0:
                    #Buy limit price hit
                    if symbol_current_low <= limit_price:
                        _fillOrder(engine, order_symbol, order_timestamp, order_type, order_side, order_size, limit_price, order_tp_points, order_sl_points)
                        engine.resting_orders.remove(order)
                        continue
                    else:
                        continue

                elif order_side == 1:
                    #Sell limit price hit
                    if symbol_current_high >= limit_price:
                        _fillOrder(engine, order_symbol, order_timestamp, order_type, order_side, order_size, limit_price, order_tp_points, order_sl_points)
                        engine.resting_orders.remove(order)
                        continue
                    else:
                        continue
            
            elif order_type == 3:
                stop_price = order_rest_price

                if order_side == 0:
                    #Buy stop price hit
                    if symbol_current_high >= stop_price:
                        _fillOrder(engine, order_symbol, order_timestamp, order_type, order_side, order_size, stop_price, order_tp_points, order_sl_points)
                        engine.resting_orders.remove(order)
                        continue
                    else:
                        continue

                elif order_side == 1:
                    #Sell stop price hit
                    if symbol_current_low <= stop_price:
                        _fillOrder(engine, order_symbol, order_timestamp, order_type, order_side, order_size, stop_price, order_tp_points, order_sl_points)
                        engine.resting_orders.remove(order)
                        continue
                    else:
                        continue
