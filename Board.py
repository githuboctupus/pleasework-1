import Snake
import stable_baselines3 as sb3
import numpy
from stable_baselines3 import DQN
class Board: #env
    #board is in reverse height order visually
    #cell format, 0=false, 1=true:
    #[isfood, isoppbody, isopphead, ismybody, ismyhead]
    def __init__(self, gamedata, snakeindex):
        self.data = gamedata
        self.width = gamedata['board']['width']
        self.height = gamedata['board']['height']
        self.grid = [[[0, 0, 0, 0, 0] for _ in range(self.width)] for _ in range(self.height)]  # None represents empty space
        self.snakes = [] #list of Snake objects
        self.foods = gamedata['board']['food']
        self.selfindex = snakeindex
        for i in range(len(gamedata['board']['snakes'])):
            snakeobj = Snake.Snake(gamedata, i)
            self.snakes.append(snakeobj)
            self.place_snake(snakeobj, i==self.selfindex)
        self.place_food(self.foods)
    def place_food(self, food_list):
        for food in food_list:
            self.grid[food['y']][food['x']] = [1, 0, 0, 0, 0]
    def add_food(self, newfood):
        self.foods.append(newfood)#dict form
        self.grid[newfood['y']][newfood['x']] = [1, 0, 0, 0, 0]
    def place_snake(self, snakeobject, isme):
        #snakeobejct is snake class
        snake_body=snakeobject.body
        snake_head=snake_body[0]#dict form
        if isme:
            self.grid[snake_head['y']][snake_head['x']] = [0, 0, 0, 0, 1]
        else:
            self.grid[snake_head['y']][snake_head['x']] = [0, 0, 1, 0, 0]
        for i in range(1, len(snake_body)):
            segment = snake_body[i]
            if isme:
                self.grid[segment['y']][segment['x']] = [0, 0, 0, 1, 0]
            else:
                self.grid[segment['y']][segment['x']] = [0, 1, 0, 0, 0]
    def move_snake(self, snakeindex, direction):
        #board has not been updated
        selectedsnake = self.snakes[snakeindex]
        dideat = selectedsnake.move(direction, self.foods)
        if dideat!=None:
            for i in range(len(self.foods)):
                if (i<len(self.foods)):
                    if (self.foods[i]['x'] == dideat['x'] and self.foods[i]['y'] == dideat['y']):
                        del self.foods[i]
        return dideat
    def update_board(self):
        for i in range(len(self.snakes)):
            self.dead_check(i)
        self.grid = [[[0, 0, 0, 0, 0] for _ in range(self.width)] for _ in range(self.height)]
        for i in range(len(self.snakes)):
            snake_obj = self.snakes[i]
            if snake_obj!=None:
                self.place_snake(snake_obj, i==self.selfindex)
        self.place_food(self.foods)
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return 'wall'  # Represents out-of-bounds as a wall
    def kill_snake(self, deadsnakeindex):
        self.snakes[deadsnakeindex]=None
        return deadsnakeindex
    def dead_check(self, snakeindex):
        #if snakelength=3 and all 3 coords in same spot, its chill
        if self.snakes[snakeindex]!=None:
            thissnake = self.snakes[snakeindex]
            if (thissnake.health<1):
                print("starvation")
                self.kill_snake(snakeindex)
            elif (thissnake.head['x']<0 or thissnake.head['x']>=self.width or thissnake.head['y']<0 or thissnake.head['y']>=self.height):
                print("oub")
                self.kill_snake(snakeindex)
            if self.snakes[snakeindex]!=None and not self.snakes[snakeindex].instartingspot():
                print("collide with self")
                myhead = self.snakes[snakeindex].head
                for i in range(len(self.snakes)):
                    if self.snakes[i]!=None:
                        currentsnakeindex = self.snakes[i]
                        thissnakebody_dict = currentsnakeindex.get_body()
                        if myhead['x'] == currentsnakeindex.head['x'] and myhead['y'] == currentsnakeindex.head['y'] and i!=snakeindex:
                            thissnakelength = thissnake.length
                            currentsnakelength = currentsnakeindex.length
                            if (thissnakelength>currentsnakelength):
                                self.kill_snake(i)
                            elif (thissnakelength<currentsnakelength):
                                self.kill_snake(snakeindex)
                            else:
                                self.kill_snake(snakeindex)
                                self.kill_snake(i)
                        for i in range(1, len(thissnakebody_dict)):
                            if thissnakebody_dict[i]['x'] == myhead['x'] and thissnakebody_dict[i]['y'] == myhead['y']:
                                self.kill_snake(snakeindex)
         
    def step(self, myaction):
        #rewards: 
        #eat+15
        #avoid danger (opphead, walls, body, deadends, etc)
        #   obvious avoidance (wall, body) +2
        #   avoided present deadend +5
        #   avoid dangerous opponent head +1
        #   stayed outside dangerous territory/avoided forced (deadend through my territory) deadend+10
        #       i will hard teach this
        #put opp in danger
        #   move to smaller opp head: +2
        #   based on worsening
        # gameloss (ded) -100
        # gamewin+100
        determinedreward=0
        myindex = self.selfindex
        dideat = self.move_snake(myindex, myaction) #determine if eated
        if dideat!=None:
            determinedreward+=2.5
        #self.update_board()
        #self.printself()
        #print("this is the board after only you made the move")
        model = DQN.load("snakemodel4")
        movelist = ['up', 'down', 'left', 'right']
        for i in range(len(self.snakes)):
            if i!=myindex and self.snakes[i]!=None:
                oppheadid = self.snakes[i].head
                #oppaction = input("Enter action (updownleftright) for snake with head "+str(oppheadid['x'])+'x, '+str(oppheadid['y'])+"y")
                oppaction, _states = model.predict(numpy.array(self.returngrid()), deterministic=True)
                #print("the opps predict:", movelist[oppaction])
                self.move_snake(i, movelist[oppaction])
        for i in range(len(self.snakes)):
            self.dead_check(i)
        self.update_board()
        return determinedreward
    def printself(self):
        print()
        for y in range(self.height):
            for x in range(self.width):
                thisspace = self.grid[self.height-y-1][x]
                try:
                    type = thisspace.index(1)
                    if type==-1:
                        print('#', end='')
                    elif type==0:
                        print('F', end='')
                    elif type==1:
                        print('B', end='')
                    elif type==2:
                        print('O', end='')
                    elif type==3:
                        print('M', end='')
                    elif type==4:
                        print('H', end='')
                except:
                    print('#', end='')
            print()
    def isjoever(self):
        if self.snakes[self.selfindex] == None:
            return True
        return False
    def iswon(self):
        alldead=True
        for i in range(len(self.snakes)):
            if (i!=self.selfindex and self.snakes[i]!=None):
                alldead=False
        return alldead
    def returngrid(self):
        return self.grid