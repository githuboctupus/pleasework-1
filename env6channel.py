import Board, Snake, json
import gymnasium
from gymnasium import spaces
import numpy
from copy import deepcopy
from time import sleep
class Env6channel(gymnasium.Env):
    def __init__(self, data):
        super(Env6channel, self).__init__()
        self.startingdata = data
        self.debug=False
        youindex=0
        for i in range(len(self.startingdata['board']['snakes'])):
            if self.startingdata['board']['snakes'][i]['id'] == self.startingdata['you']['id']:
                youindex=i
        self.boardobject = Board.Board(self.startingdata, youindex)
        self.action_space = spaces.Discrete(4)  # 0: up, 1: down, 2: left, 3: right
        self.observation_space = spaces.Box(low=0, high=255, shape=(6, 13, 13), dtype=numpy.uint8)
        self.reset()
    def reset(self, seed=None):
        youindex=0
        for i in range(len(self.startingdata['board']['snakes'])):
            if self.startingdata['board']['snakes'][i]['id'] == self.startingdata['you']['id']:
                youindex=i
        self.boardobject = Board.Board(self.startingdata, youindex)
        # foodgrid = numpy.array(self.boardobject.returngridjustfood())
        # selfgrid = numpy.array(self.boardobject.returngridjustself())
        # oppgrid = numpy.array(self.boardobject.returngridjustopps())
        observation = self.boardobject.return6channel()
        if self.debug:
            self.render()
            print("resetted")
        return observation, {}
    def step(self, action):
        if self.debug:
            sleep(0.5)
        convertedaction=''
        if action==0:
            convertedaction='up'
        if action==1:
            convertedaction='down'
        if action==2:
            convertedaction='left'
        if action==3:
            convertedaction='right'
        #print("MYACTION", convertedaction)
        reward=1.0#give more guidance rewards
        #previousboardstate = numpy.array(deepcopy(self.boardobject.returngrid()), dtype=numpy.float32)
        reward+=self.boardobject.step(convertedaction)
        #observation = self.boardobject.returngrid()
        # foodgrid = numpy.array(self.boardobject.returngridjustfood())
        # selfgrid = numpy.array(self.boardobject.returngridjustself())
        # oppgrid = numpy.array(self.boardobject.returngridjustopps())
        observation = self.boardobject.return6channel()
        if self.debug:
            self.render()
            print("final board returned for observation (after action)")
        #reward = float(input("Enter a FLOAT reward for yousnake's move (resulting in observation):"))
        done=self.boardobject.isjoever()
        if (done):
            if self.debug:
                print("JOEVER")
            reward=-100.0
            done=True
        elif (self.boardobject.iswon()):
            print("WON")
            if self.debug:
                print("WON")
            reward=160.0
            done=True
        #print("Reward:", reward)
        #when server startsdone=True
        return observation, reward, done, False, {}
    def render(self):
        self.boardobject.return6channel(justrender=True)
    def returnmygrid(self):
        return self.boardobject.return6channel()