###------EXAMPLE------###

#STD
#TP
import pandas as pd
import talib
#LCL
from user.data.get_data import get_data
from bt_engine import engine
from user.strategies.strategy1 import Strategy1

#Pull data
es_df = get_data(symbol='ES.v.0')
nq_df = get_data(symbol='NQ.v.0')

#Align timestamps
df = pd.merge(es_df, nq_df, on='timestamp', how='inner', suffixes=('_es', '_nq'))
es_df = df[['timestamp', 'open_es', 'high_es', 'low_es', 'close_es', 'volume_es']]
es_df = es_df.rename(columns={'open_es': 'open', 'high_es': 'high', 'low_es': 'low', 'close_es': 'close', 'volume_es': 'volume'})
nq_df = df[['timestamp', 'open_nq', 'high_nq', 'low_nq', 'close_nq', 'volume_nq']]
nq_df = nq_df.rename(columns={'open_nq': 'open', 'high_nq': 'high', 'low_nq': 'low', 'close_nq': 'close', 'volume_nq': 'volume'})

#Calculate indicators
es_ema = talib.EMA(es_df['close'], timeperiod=90)
nq_ema = talib.EMA(nq_df['close'], timeperiod=90)

data = {
    'es': {
        'tick_size': 0.25,
        'tick_value': 12.50,
        'commission': 2.80,
        'fixed_slippage': 14.00,
        'dataframe': es_df,
        'ema': es_ema
    },
    'nq': {
        'tick_size': 0.25,
        'tick_value': 5.00,
        'commission': 2.80,
        'fixed_slippage': 24.00,
        'dataframe': nq_df,
        'ema': nq_ema
    }
}

test = engine.Engine(data, 50000)
test.startBacktest(Strategy1(), 'backtest_saves/test1')
