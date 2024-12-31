import Board, Snake, json
import gymnasium
from gymnasium import spaces
import numpy
from copy import deepcopy
class Env(gymnasium.Env):
    def __init__(self, data):
        super(Env, self).__init__()
        self.startingdata = data
        self.boardobject = Board.Board(self.startingdata)
        self.action_space = spaces.Discrete(4)  # 0: up, 1: down, 2: left, 3: right
        self.observation_space = spaces.Box(low=0, high=1, shape=(11, 11, 5), dtype=numpy.float32)
        self.reset()
    def reset(self, seed=None):
        self.boardobject = Board.Board(self.startingdata)
        grid_np = numpy.array(self.boardobject.returngrid(), dtype=numpy.float32)
        self.render()
        return grid_np, {}
    def step(self, action):
        convertedaction=''
        if action==0:
            convertedaction='up'
        if action==1:
            convertedaction='down'
        if action==2:
            convertedaction='left'
        if action==3:
            convertedaction='right'
        print("ACTION", convertedaction)
        #previousboardstate = numpy.array(deepcopy(self.boardobject.returngrid()), dtype=numpy.float32)
        self.boardobject.step(convertedaction)
        #observation = self.boardobject.returngrid()
        observation_np = numpy.array(deepcopy(self.boardobject.returngrid()), dtype=numpy.float32)
        self.render()
        print("final board")
        reward = float(input("Enter a FLOAT reward for yousnake's move (resulting in observation):"))
        done=self.boardobject.isjoever()
        return observation_np, reward, done, False, {}
    def render(self):
        self.boardobject.printself()

    