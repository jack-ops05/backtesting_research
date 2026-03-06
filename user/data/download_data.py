###------DOWNLOAD DATA WITH DATABENTO API------###

#STD
#TP
import databento as db
import sqlite3
#LCL

api_key = input('Paste DataBento Api-Key: ')
client = db.Historical(api_key)
data = client.timeseries.get_range(
    dataset='GLBX.MDP3',
    start='2015-01-01T00:00:00',
    end='2025-12-31T23:59:00',
    symbols=['NQ.v.0'],
    schema='ohlcv-1m',
    stype_in='continuous'
)
df = data.to_df()
df = df.reset_index()
df = df.rename(columns={'ts_event': 'timestamp'})
df = df[['symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume']]

with sqlite3.connect('user/data/data.db') as conn:
    df.to_sql('ohlcv_1m', conn, if_exists='append', index=False)
