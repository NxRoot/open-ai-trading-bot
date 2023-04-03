import pandas as pd
import indicators
import requests
import os

def Binance(symbol = "BTCUSDT", interval = "4h", limit = 10000):

    # Create directory
    dataPath = "data"
    modelPath = f"{dataPath}/{symbol}_{interval}_{str(limit)}"
    if not os.path.exists(dataPath): os.makedirs(dataPath)

    url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}'
    data = requests.get(url).json()

    columns = [
        # Used columns
        'timestamp', 'open', 'high', 'low', 'close', 'volume', 'number_of_trades',
        # Ignored columns
        'close_time', 
        'quote_asset_volume', 
        'taker_buy_base_asset_volume', 
        'taker_buy_quote_asset_volume', 
        'ignore'
    ]

    df = pd.DataFrame(data, columns=columns)
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('timestamp', inplace=True)
    df = df[['open', 'high', 'low', 'close', 'volume']]
    df = df.astype(float)

    df['macd'] = indicators.MACD(df['close'])
    df['rsi'] = indicators.RSI(df['close'])

    return df, modelPath
