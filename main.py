import Board
import Snake
import json
import stable_baselines3 as sb3 #TODO: maybe transition to pytorch and use cnn
import env
import env5by5
import env3channel
import env6channel
import numpy
from stable_baselines3 import DQN, PPO
from stable_baselines3.common.evaluation import evaluate_policy
import torch as th
from torch import nn
from stable_baselines3.common.torch_layers import BaseFeaturesExtractor
from gymnasium import spaces
data={"game":{"id":"b490893a-6166-4101-9926-48c13c0bb623","ruleset":{"name":"standard","version":"v1.2.3","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":0,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":0},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":"custom"},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"gs_qPYhgmryTb9bttDPWVQJc663","name":"snake","latency":"","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#888888","head":"default","tail":"default"}},{"id":"gs_GRwqhb6dtdPTX6Cw7HF8869Q","name":"Hungry Bot","latency":"","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00cc00","head":"alligator","tail":"alligator"}}],"food":[{"x":0,"y":6},{"x":10,"y":6},{"x":5,"y":5}],"hazards":[]},"you":{"id":"gs_qPYhgmryTb9bttDPWVQJc663","name":"snake","latency":"","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#888888","head":"default","tail":"default"}}}
data_solo = {"game":{"id":"849055","ruleset":{"name":"standard","version":"v.1.2.3"},"timeout":500},"turn":3,"you":{"health":100,"id":"you","name":"#22aa34","body":[{"x":3,"y":6},{"x":3,"y":5},{"x":3,"y":4}],"head":{"x":3,"y":6},"length":3},"board":{"food":[{"x":7,"y":6}],"height":11,"width":11,"snakes":[{"health":100,"id":"you","name":"#22aa34","body":[{"x":3,"y":6},{"x":3,"y":5},{"x":3,"y":4}],"head":{"x":3,"y":6},"length":3}]}}
data_solo_corner = {"game":{"id":"902484","ruleset":{"name":"standard","version":"v.1.2.3"},"timeout":500},"turn":200,"you":{"health":100,"id":"you","name":"#22aa34","body":[{"x":0,"y":10},{"x":1,"y":10},{"x":2,"y":10}],"head":{"x":0,"y":10},"length":3},"board":{"food":[{"x":1,"y":5},{"x":7,"y":3},{"x":7,"y":4},{"x":5,"y":7},{"x":4,"y":3}],"height":11,"width":11,"snakes":[{"health":100,"id":"you","name":"#22aa34","body":[{"x":0,"y":10},{"x":1,"y":10},{"x":2,"y":10}],"head":{"x":0,"y":10},"length":3}]}}
data_solo_5by5={"game":{"id":"849055","ruleset":{"name":"standard","version":"v.1.2.3"},"timeout":500},"turn":200,"you":{"health":100,"id":"you","name":"#22aa34","body":[{"x":1,"y":0},{"x":0,"y":0},{"x":0,"y":1}],"head":{"x":1,"y":0},"length":3},"board":{"food":[{"x":0,"y":3},{"x":2,"y":2}],"height":5,"width":5,"snakes":[{"health":100,"id":"you","name":"#22aa34","body":[{"x":1,"y":0},{"x":0,"y":0},{"x":0,"y":1}],"head":{"x":1,"y":0},"length":3}]}}
#envir = env5by5.Env5by5(data_solo_5by5)
#envir = env.Env(data_solo_corner)
envir = env6channel.Env6channel(data)
# model = DQN(
#     "MlpPolicy",
#     envir,
#     exploration_initial_eps=1.0,
#     exploration_fraction=0.3,
#     exploration_final_eps=0.10,
#     verbose=2,
#     tensorboard_log="./ppo_battlesnake_tensorboard/"
#     )
class CustomCNN(BaseFeaturesExtractor):
    def __init__(self, observation_space: spaces.Box, features_dim: int = 512):
        super(CustomCNN, self).__init__(observation_space, features_dim)
        # Observation space dimensions
        input_channels = observation_space.shape[0]  # Number of grids (6)
        height, width = observation_space.shape[1:]  # Grid size (13x13)
        
        # Define the CNN
        self.cnn = nn.Sequential(
            nn.Conv2d(input_channels, 32, kernel_size=3, stride=1, padding=1),  # Output: (32, 13, 13)
            nn.ReLU(),
            nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),              # Output: (64, 7, 7)
            nn.ReLU(),
            nn.Conv2d(64, 128, kernel_size=3, stride=2, padding=1),             # Output: (128, 4, 4)
            nn.ReLU(),
        )

        # Calculate the flattened size after convolutions
        with th.no_grad():
            sample_input = th.zeros((1, input_channels, height, width))
            n_flatten = self.cnn(sample_input).view(1, -1).shape[1]

        # Fully connected layer to map to features_dim
        self.fc = nn.Sequential(
            nn.Linear(n_flatten, features_dim),
            nn.ReLU()
        )

    def forward(self, observations: th.Tensor) -> th.Tensor:
        cnn_out = self.cnn(observations)
        return self.fc(cnn_out.view(cnn_out.size(0), -1))
policy_kwargs = dict(
    features_extractor_class=CustomCNN,
    features_extractor_kwargs=dict(features_dim=256),  # Adjust features_dim as needed
)
# model = PPO(
#     "CnnPolicy",
#     envir,
#     verbose=2,
#     n_steps=1024,
#     gamma=0.999,
#     batch_size=64,
#     ent_coef=0.25,
#     policy_kwargs=policy_kwargs
# )
model = PPO.load("snakemodel_cnn_1.0.0", env=envir)
#model.ent_coef=0.5 #explorer
#model.ent_coef=0.35#hybrid-explorer
#model.ent_coef = 0.2 #less explorer but still kinda
#model.ent_coef=0.15
#model.ent_coef = 0.05 #more deterministic
model.learn(total_timesteps=50000, progress_bar=True)

# Save the model after training
#dc=don't crash
model.save("snakemodel_cnn_1.0.0")
envir.reset()
# mean_reward, std_reward = evaluate_policy(
#     model, 
#     envir, 
#     n_eval_episodes=10,  # Number of episodes to evaluate
#     render=False         # Set to True if you want to visualize the evaluation
# )
# print("mean reward", mean_reward)
# print("std reward", std_reward)