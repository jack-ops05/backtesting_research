#STD
import time
from pathlib import Path
import os
#TP
#LCL
from bt_engine.orders.updateOrders import _updateOrders
from bt_engine.positions.updatePositions import _updatePositions
from bt_engine.utils.calcPerformance import _calcPerformance
from bt_engine.utils.liquidateAccount import _liquidateAccount

def _startBacktest(engine, strategy_instance, save_dir):
    #Purpose of function: To start the backtest simulation by iterating over a range equal to the length of the DataFrames. Calls strategy logic, as well as order and position updates.

    if Path.exists(Path(save_dir)):
        raise ValueError('Save directory already exists')
    else:
        engine.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    for row in range(1, engine.row_length):
        engine.current_row = row

        if engine.balance <= 0:
            _liquidateAccount(engine)
            break

        _updateOrders(engine)
        _updatePositions(engine)
        strategy_instance.on_row(engine)

    _calcPerformance(engine)
