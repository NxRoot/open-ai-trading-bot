import numpy as np
import gym

class MarketEnv(gym.Env):
    def __init__(self, data):
        self.data = data
        self.action_space = gym.spaces.Discrete(3)
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(len(data.columns),))
        self.reset()

    def reset(self):
        self.t = 0
        self.profit = 0
        self.bought = False
        self.cost = 0
        return self.data.iloc[self.t].values
    
    def step(self, action):
        current_close = self.data.iloc[self.t]['close']
        self.t += 1
        reward = 0
        
        if action == 0: # Buy
            if not self.bought:
                self.bought = True
                self.cost = current_close
        elif action == 1: # Sell
            if self.bought:
                self.bought = False

                if(current_close > self.cost):
                    self.profit = current_close - self.cost
                else:
                    self.profit = self.profit - (self.cost - current_close)
                
                self.cost = 0
        else: # Hold
            pass
        
        done = (self.t == len(self.data) - 1)
        reward = self.profit
        obs = self.data.iloc[self.t].values
        
        return obs, reward, done, {}