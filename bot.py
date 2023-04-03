from stable_baselines3 import DQN
import sys

def train(env, modelPath, iterations = 1000000):
    # Create new model
    model = DQN('MlpPolicy', env, verbose=1)
    # Train the agent
    print("Training: Please wait...\n")
    model.learn(total_timesteps=iterations, log_interval=100)
    # Save the trained model to file
    model.save(f'{modelPath}.zip')
    print("Training: Complete!\n")

def predict(env, modelPath):
    # Load the saved model from file
    model = DQN.load(f'{modelPath}.zip')
    # Evaluate the agent
    obs = env.reset()
    result = 0
    buys = 0
    sells = 0
    while True:
        action, _states = model.predict(obs)
        obs, reward, done, info = env.step(action)
        result += reward
        if(action == 0): buys += 1
        if(action == 1): sells += 1

        if done: break

    print(f"\nProfit: {round(result, 2)}")
    print(f"Buy: {buys}")
    print(f"Sell: {sells}\n")
