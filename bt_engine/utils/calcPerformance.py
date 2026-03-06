#STD
#TP
import pandas as pd
import numpy as np
import json
#LCL
from bt_engine.utils.plotEquity import _plotEquity

def _calcPerformance(engine):
    #Purpose of function: To calculate and save performance at the end of backtest.

    trade_log_df = pd.DataFrame(engine.trade_log)
    trade_log_df.to_csv(f'{engine.save_dir}/trade_log.csv')

    #Equity curve
    x_array = trade_log_df['exit_timestamp'].values
    x_array = np.insert(x_array, 0, engine.timestamps[0])
    y_array = trade_log_df['equity'].values
    y_array = np.insert(y_array, 0, engine.starting_balance)
    _plotEquity(x_array, y_array)

    #For win rate/profit factor/expected value
    wins = []
    losses = []
    durations = []
    for trade in engine.trade_log:
        pnl = trade['pnl']
        durations.append(trade['exit_bar'] - trade['entry_bar'])

        if pnl > 0:
            wins.append(pnl)

        elif pnl < 0:
            losses.append(pnl)
    winning_trades = len(wins)
    losing_trades = len(losses)
    gross_wins = sum(wins)
    gross_losses = abs(sum(losses))

    #For max dd
    peak = float('-inf')
    max_dd = 0
    for equity in y_array:

        if equity > peak:
            peak = equity

        drawdown = (equity - peak) / peak

        if drawdown < max_dd:
            max_dd = drawdown

    #Final metrics
    total_trades = len(engine.trade_log)
    avg_trade_duration = sum(durations) / len(durations) if durations else 0
    net_pnl = engine.balance - engine.starting_balance
    win_rate = winning_trades / total_trades if total_trades else 0
    loss_rate = 1 - win_rate
    avg_win = gross_wins / winning_trades if wins else 0
    largest_win = max(wins) if wins else 0
    avg_loss = gross_losses / losing_trades if losses else 0
    largest_loss = min(losses) if losses else 0
    profit_factor = gross_wins / gross_losses if gross_losses else 0
    expected_value = (win_rate * avg_win) + (loss_rate * avg_loss)
    max_drawdown = abs(max_dd)

    metrics = {
        'total_trades': total_trades,
        'avg_trade_duration': round(avg_trade_duration, 2),
        'net_pnl': round(net_pnl, 2),
        'win_rate_pct': round(win_rate * 100, 2),
        'avg_win': round(avg_win, 2),
        'largest_win': round(largest_win, 2),
        'avg_loss': round(avg_loss, 2),
        'largest_loss': round(largest_loss, 2),
        'profit_factor': round(profit_factor, 2),
        'expected_value': round(expected_value, 2),
        'max_drawdown_pct': round(max_drawdown * 100, 2),
    }

    with open(f'{engine.save_dir}/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
