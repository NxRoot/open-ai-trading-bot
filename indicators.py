def RSI(close, timeframe=14):
    # Calculate RSI
    delta = close.diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)
    avg_gain = gain.rolling(window=timeframe).mean()
    avg_loss = loss.rolling(window=timeframe).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def MACD(close, timeframe=12):
    # Calculate MACD
    ema_12 = close.ewm(span=timeframe, adjust=False).mean()
    ema_26 = close.ewm(span=26, adjust=False).mean()
    macd = ema_12 - ema_26
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return macd

def DX(high, low, close, timeframe=12):
    # Calculate the positive and negative directional indicators
    up = high.diff()
    down = low.diff().abs()
    pos_di = 100 * up.ewm(span=timeframe).mean() / close
    neg_di = 100 * down.ewm(span=timeframe).mean() / close
    
    # Calculate the DX
    dx = 100 * (pos_di - neg_di).abs() / (pos_di + neg_di)
    return dx.rolling(window=14).mean()
