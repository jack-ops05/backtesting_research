#STD
#TP
#LCL
from bt_engine.positions.closePosition import _closePosition
from bt_engine.utils.liquidateAccount import _liquidateAccount

def _updatePositions(engine):
    #Purpose of function: To update any open positions by checking if the positions stop loss or take profit has been hit. If not, calculates all positions open pnl's.

    if len(engine.positions) > 0:

        pnls = []
        for pos in engine.positions.copy():
            
            #Position lookups
            pos_id = pos['position_id']
            pos_symbol = pos['symbol']
            pos_entry_price = pos['entry_price']
            pos_side = pos['side']
            pos_size = pos['size']
            pos_tp = pos['tp']
            pos_sl = pos['sl']

            #Symbol lookups
            symbol_data = engine.market_data[pos_symbol]
            symbol_current_high = symbol_data['h'][engine.current_row]
            symbol_current_low = symbol_data['l'][engine.current_row]
            symbol_current_close = symbol_data['c'][engine.current_row]
            symbol_tick_size = symbol_data['tick_size']
            symbol_tick_value = symbol_data['tick_value']

            #Check stop loss
            if pos_sl != None:

                #Long position
                if pos_side == 0:
                    if symbol_current_low <= pos_sl:
                        _closePosition(engine, pos_id, pos_sl)
                        continue

                #Short position
                elif pos_side == 1:
                    if symbol_current_high >= pos_sl:
                        _closePosition(engine, pos_id, pos_sl)
                        continue

            #Check take profit
            if pos_tp != None:

                #Long position
                if pos_side == 0:
                    if symbol_current_high >= pos_tp:
                        _closePosition(engine, pos_id, pos_tp)
                        continue

                #Short position
                elif pos_side == 1:
                    if symbol_current_low <= pos_tp:
                        _closePosition(engine, pos_id, pos_tp)
                        continue

            #Calculate open pnl
            if pos_side == 0:
                open_ticks = (symbol_current_close - pos_entry_price) / symbol_tick_size
                pos_pnl = open_ticks * symbol_tick_value * pos_size
                pnls.append(pos_pnl)

            elif pos_side == 1:
                open_ticks = (pos_entry_price - symbol_current_close) / symbol_tick_size
                pos_pnl = open_ticks * symbol_tick_value * pos_size
                pnls.append(pos_pnl)

        engine.open_pnl = sum(pnls)
        if engine.open_pnl + engine.balance <= 0:
            _liquidateAccount(engine)
