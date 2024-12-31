import Board, Snake, json
import gym
from gym import spaces
import numpy
class Env(gym.Env):
    def __init__(self, data):
        super(Env, self).__init__()
        self.startingdata = data
        self.boardobject = Board.Board(self.startingdata)
        self.action_space = spaces.Discrete(4)  # 0: up, 1: down, 2: left, 3: right
        self.observation_space = spaces.Box(low=0, high=1, shape=(11, 11, 5), dtype=numpy.float32)
    def reset(self):
        self.boardobject = Board.Board(self.startingdata)
    def step(self, action):
        previousboardstate = self.boardobject.returngrid().deepcopy()
        self.boardobject.step(action)
        observation = self.boardobject.returngrid()
        reward = float(input("Enter a FLOAT reward for yousnake's move (resulting in observation):"))
        done=self.boardobject.isjoever()
        return observation, reward, done
    def render(self):
        self.boardobject.printself()

    