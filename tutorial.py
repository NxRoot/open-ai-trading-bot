#---------------------------#
# DEFAULT BOT CONFIGURATION #
#---------------------------#
import os

symbol = "BTCUSDT"
interval = "1h"
datalimit = 10000

logs = "logs"
models = "models"
tablePath = f'{symbol}_{interval}.csv'
modelPath = f'{symbol}_{interval}.zip'

if not os.path.exists(logs): os.makedirs(logs)
if not os.path.exists(models): os.makedirs(models)

#-------------------------------#
# FETCH DATA FROM API (Binance) #
#-------------------------------#

import requests
import pandas as pd

url = f'https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={datalimit}'
data = requests.get(url).json()
df = pd.DataFrame(data, columns=[
    # Used columns
    'timestamp', 'open', 'high', 'low', 'close', 'volume',
    # Ignored columns
    'number_of_trades',
    'close_time', 
    'quote_asset_volume', 
    'taker_buy_base_asset_volume', 
    'taker_buy_quote_asset_volume', 
    'ignore'
])
data = df[['open', 'high', 'low', 'close', 'volume']].astype(float) # Original data (current)
norm_data = (data - data.min()) / (data.max() - data.min()) # Normalized data (optional)

### DEBUG ONLY (save data to csv) (optional)
data.to_csv(f"{models}/original_{tablePath}", index=False)
norm_data.to_csv(f"{models}/{tablePath}", index=False)

#----------------------------#
# CREATE TRADING ENVIRONMENT #
#----------------------------#

import gym
import numpy as np

class BuySell(gym.Env):
    def __init__(self, data):
        self.data = data
        # Define boundaries
        actions = 3
        minValue = -np.inf
        maxValue = np.inf
        columns = len(self.data.columns)
        # Define action and observation spaces
        self.action_space = gym.spaces.Discrete(actions) # HOLD, BUY, SELL
        self.observation_space = gym.spaces.Box(low=minValue, high=maxValue, shape=(columns,))
        self.reset()

    def reset(self):
        # Default values
        self.t = 0
        self.bought = False
        self.cost = 0
        return self.data.iloc[self.t].values
    
    def step(self, action):

        # Required Values
        current = self.data.iloc[self.t]
        reward = 0

        # Display values
        order = "HOLD"
        dd = 0
        
        # Apply market strategy

        if action == 0: # HOLD
            pass

        elif action == 1: # BUY
            if not self.bought:
                order = "BUY"
                self.cost = current['close']
                self.bought = True

        elif action == 2: # SELL
            if self.bought and current['close'] - self.cost > 0:
                order = "SELL"
                reward = current['close'] - self.cost
                self.bought = False

        # Calculate Drawdown
        if current['close'] < self.cost and self.bought:
            dd = self.cost - current['close']
            

        # Update step
        done = (self.t == len(self.data) - 1)
        obs = self.data.iloc[self.t].values
        self.t += 1

        # Return observation
        return obs, reward, done, {
            "action": order,
            "price": float(current['close']),
            "cost": float(self.cost),
            "profit": float(reward),
            "drawdown": float(dd),
        }


#-----------------------#
# CREATE TRAINING MODEL #
#-----------------------#

# Test out different models from stable_baselines3 (current: DQN)
from stable_baselines3 import PPO, DQN, A2C  

# Create Environment
strategy = BuySell(data)
iterations = 1000000

model = "DQN" 
path = f"{models}/{model}_{modelPath}"

# Create or load model
if not os.path.exists(path):
    # Create
    model = DQN('MlpPolicy', strategy, verbose=1, tensorboard_log=logs)
    # Train
    model.learn(total_timesteps=iterations, reset_num_timesteps=False)
    # Save
    model.save(path)
else:
    # Load 
    model = DQN.load(path)


#-------------------#
# MARKET PREDICTION #
#-------------------#

obs = strategy.reset()
profit = 0
drawdown = []
done = False

# Make Prediction
while True:
    action, _states = model.predict(obs)
    obs, reward, done, info = strategy.step(action)
    profit += info['profit']
    drawdown.append(info['drawdown'])
    print(info)
    if done: break

print()
print("Ticker:", symbol)
print("Total Profit:", profit)
print("Max Drawdown:", max(drawdown))
print()
