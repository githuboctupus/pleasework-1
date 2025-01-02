import Board
import Snake
import json
import stable_baselines3 as sb3
import env
import numpy
from stable_baselines3 import DQN
#TODO: why always collide with self?
data={"game":{"id":"b490893a-6166-4101-9926-48c13c0bb623","ruleset":{"name":"standard","version":"v1.2.3","settings":{"foodSpawnChance":15,"minimumFood":1,"hazardDamagePerTurn":0,"hazardMap":"","hazardMapAuthor":"","royale":{"shrinkEveryNTurns":0},"squad":{"allowBodyCollisions":False,"sharedElimination":False,"sharedHealth":False,"sharedLength":False}}},"map":"standard","timeout":500,"source":"custom"},"turn":0,"board":{"height":11,"width":11,"snakes":[{"id":"gs_qPYhgmryTb9bttDPWVQJc663","name":"snake","latency":"","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#888888","head":"default","tail":"default"}},{"id":"gs_GRwqhb6dtdPTX6Cw7HF8869Q","name":"Hungry Bot","latency":"","health":100,"body":[{"x":9,"y":5},{"x":9,"y":5},{"x":9,"y":5}],"head":{"x":9,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#00cc00","head":"alligator","tail":"alligator"}}],"food":[{"x":0,"y":6},{"x":10,"y":6},{"x":5,"y":5}],"hazards":[]},"you":{"id":"gs_qPYhgmryTb9bttDPWVQJc663","name":"snake","latency":"","health":100,"body":[{"x":1,"y":5},{"x":1,"y":5},{"x":1,"y":5}],"head":{"x":1,"y":5},"length":3,"shout":"","squad":"","customizations":{"color":"#888888","head":"default","tail":"default"}}}
envir = env.Env(data)
# model = DQN(
#     "MlpPolicy",
#     envir,
#     exploration_initial_eps=1.0,
#     exploration_fraction=0.25,
#     exploration_final_eps=0.15,
#     verbose=2,
#     tensorboard_log="./ppo_battlesnake_tensorboard/"
#     )
model = DQN.load("snakemodel4", env=envir)
model.learn(total_timesteps=50, progress_bar=True)

# Save the model after training
model.save("snakemodel1")
envir.reset()
action, _states = model.predict(numpy.array(envir.returnmygrid()), deterministic=False)
print(action)
