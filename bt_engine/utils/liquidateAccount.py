#STD
#TP
#LCL
from bt_engine.orders.cancelOrder import _cancelOrder
from bt_engine.positions.closePosition import _closePosition

def _liquidateAccount(engine):
    #Purpose of function: To liquidate account.

    if len(engine.resting_orders) > 0:
        for order in engine.resting_orders.copy():
            _cancelOrder(engine, order['order_id'])
            continue
    
    if len(engine.positions) > 0:
        for pos in engine.positions.copy():
            _closePosition(engine, pos['position_id'], None)
            continue
