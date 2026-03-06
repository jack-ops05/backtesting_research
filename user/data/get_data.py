#STD
#TP
import pandas as pd
import sqlite3
#LCL

#CURRENT AVAILABLE SYMBOLS IN user/data/data.db: ES.v.0 | NQ.v.0

def get_data(symbol):
    with sqlite3.connect('user/data/data.db') as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM ohlcv_1m WHERE symbol = ? AND timestamp > 2025;', (symbol,))
        data = cur.fetchall()
    df = pd.DataFrame(data, columns=('symbol', 'timestamp', 'open', 'high', 'low', 'close', 'volume'))
    return df
