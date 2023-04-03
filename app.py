from model import MarketEnv
import bot
import sys

# Show debug logs
import logging
logging.basicConfig(level=logging.DEBUG)

# Get data (from Binance)
import fetch 
data, modelPath = fetch.Binance("BTCUSDT", "4h")

# Normalize data
data_norm = (data - data.mean()) / data.std()
data_norm = data_norm.fillna(0)

# Create environment
env = MarketEnv(data_norm)
    
# Execute command
if(len(sys.argv) > 1):

    if(sys.argv[1] == "train"): 
        bot.train(env, modelPath)

    elif(sys.argv[1] == "predict"): 
        bot.predict(env, modelPath)

else:
    bot.train(env, modelPath)
    bot.predict(env, modelPath)
    
