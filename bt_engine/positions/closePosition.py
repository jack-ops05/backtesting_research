#STD
#TP
#LCL

def _closePosition(engine, position_id, close_price):
    #Purpose of function: To close positions by removing them from the engine.positions list, calculating trade pnl, and appending the round trip trade to engine.trade_log
    
    #Find position by id
    position = None
    for pos in engine.positions:
        if position_id == pos['position_id']:
            position = pos
            break
    if position == None:
        print('ERROR: Failed to close position, could not find position id.')
        return
    
    #Position lookups
    pos_symbol = position['symbol']
    pos_side = position['side']
    pos_size = position['size']
    pos_entry_price = position['entry_price']
    pos_entry_timestamp = position['entry_timestamp']
    pos_entry_bar = position['entry_bar']

    #Symbol lookups
    symbol_data = engine.market_data[pos_symbol]
    symbol_current_close = symbol_data['c'][engine.current_row]
    symbol_tick_size = symbol_data['tick_size']
    symbol_tick_value = symbol_data['tick_value']
    symbol_commission = symbol_data['commission']
    symbol_fixed_slippage = symbol_data['fixed_slippage']

    if close_price == None:
        close_price = symbol_current_close
    
    #Calculate pnl
    if pos_side == 0:
        ticks = (close_price - pos_entry_price) / symbol_tick_size
        pnl = (ticks * symbol_tick_value * pos_size) - (symbol_commission + symbol_fixed_slippage)
    elif pos_side == 1:
        ticks = (pos_entry_price - close_price) / symbol_tick_size
        pnl = (ticks * symbol_tick_value * pos_size) - (symbol_commission + symbol_fixed_slippage)

    engine.balance += pnl
    
    #Add/remove trade
    trade = {
        'symbol': pos_symbol,
        'side': pos_side,
        'size': pos_size,
        'entry_price': pos_entry_price,
        'entry_timestamp': pos_entry_timestamp,
        'entry_bar': pos_entry_bar,
        'exit_price': close_price,
        'exit_timestamp': engine.timestamps[engine.current_row],
        'exit_bar': engine.current_row,
        'pnl': pnl,
        'commission': symbol_commission,
        'slippage': symbol_fixed_slippage,
        'equity': engine.balance
    }
    engine.trade_log.append(trade)
    engine.positions.remove(position)
