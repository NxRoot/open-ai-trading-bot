# OpenAI Trading Bot (Minimal)

* This is a simple bot to make `HOLD`, `BUY` or `SELL` orders based on market price.
* [stable-baselines](https://stable-baselines3.readthedocs.io/) is used to provide multiple [algorithmic models](https://stable-baselines3.readthedocs.io/en/master/guide/algos.html) for reinforcement learning.
* [OpenAI](https://github.com/openai/gym) is used to create a **trading environment** for machine learning.




## How to Install
```sh
# clone project
git clone https://github.com/NxRoot/open-ai-trading-bot.git

# Go to folder
cd open-ai-trading-bot

# Create Virtual Environment
python3 -m venv venv

# Activate Virtual Environment
source venv/bin/activate

# Install Required Modules
pip install -r requirements.txt
```

## How to Use

> Activate the Virtual Environment before running.

#### Run Bot
```
python3 tutorial.py
```

#### Output
```
{'action': 'HOLD', 'price': 27880.27, 'cost': 28587.64, 'profit': 0.0, 'drawdown': 707.369999999999}
{'action': 'HOLD', 'price': 27903.24, 'cost': 28587.64, 'profit': 0.0, 'drawdown': 684.3999999999978}
{'action': 'HOLD', 'price': 27956.76, 'cost': 28587.64, 'profit': 0.0, 'drawdown': 630.880000000001}
{'action': 'HOLD', 'price': 28023.39, 'cost': 28587.64, 'profit': 0.0, 'drawdown': 564.25}
{'action': 'HOLD', 'price': 27982.59, 'cost': 28587.64, 'profit': 0.0, 'drawdown': 605.0499999999993}

Ticker: BTCUSDT
Total Profit: 5842.9000000000015
Max Drawdown: 2798.0499999999993
```
> **Note**
> The Strategy used in this example is **not reallistic** and is not meant to be used as a real trading strategy.
> <br>Feel free to **create your own strategy** to fit your own needs.


#### Check Tensorboard graphs
```
tensorboard --logdir=logs
```
