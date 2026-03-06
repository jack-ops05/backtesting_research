#STD
#TP
import numpy as np
#LCL
from bt_engine.orders.placeOrder import _placeOrder
from bt_engine.orders.cancelOrder import _cancelOrder
from bt_engine.positions.closePosition import _closePosition
from bt_engine.utils.startBacktest import _startBacktest

class Engine:
    def __init__(self, market_data: dict, starting_balance: int):

        self.market_data = market_data
        self.timestamps = None

        #Configure each symbols data
        for data in self.market_data.values():

            symbol_df = data['dataframe']

            if self.timestamps is None:
                self.timestamps = symbol_df['timestamp'].values
                self.row_length = len(symbol_df)
            else:
                if len(symbol_df) != self.row_length:
                    raise ValueError('All DataFrames must be of equal length')
                if not np.array_equal(self.timestamps, symbol_df['timestamp'].values):
                    raise ValueError('DataFrames timestamps must be aligned.')

            #Convert DataFrame to NumPy arrays
            data['o'] = symbol_df['open'].values
            data['h'] = symbol_df['high'].values
            data['l'] = symbol_df['low'].values
            data['c'] = symbol_df['close'].values
            data['v'] = symbol_df['volume'].values
            del data['dataframe']

        self.current_row = None
        self.starting_balance = starting_balance
        self.balance = starting_balance
        self.resting_orders = []
        self.filled_orders = []
        self.positions = []
        self.open_pnl = 0
        self.trade_log = [] 
        self.save_dir = None

    def placeOrder(self, symbol: str, type: int, side: int, size: int, limit_price: float = None, stop_price: float = None, tp_points: float = None, sl_points: float = None):
        _placeOrder(self, symbol, type, side, size, limit_price, stop_price, tp_points, sl_points)

    def cancelOrder(self, order_id: str):
        _cancelOrder(self, order_id)

    def closePosition(self, position_id: str, close_price: float = None):
        _closePosition(self, position_id, close_price)
        
    def startBacktest(self, strategy_instance: object, save_dir: str):
        _startBacktest(self, strategy_instance, save_dir)
