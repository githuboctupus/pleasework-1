import Snake
import stable_baselines3 as sb3
import numpy
from stable_baselines3 import PPO
import random
from copy import deepcopy
class Board: #env
    #board is in reverse height order visually
    #cell format, 0=false, 1=true:
    #new format[isfood, istail, isbody, isopphead, ismyhead]
    def __init__(self, gamedata, snakeindex):
        self.debug=False
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
        if isme:#myhead
            self.grid[snake_head['y']][snake_head['x']] = [0, 0, 0, 0, 1]
        else:#opphead
            self.grid[snake_head['y']][snake_head['x']] = [0, 0, 0, 1, 0]
        for i in range(1, len(snake_body)):
            segment = snake_body[i]
            if isme:
                if i==len(snake_body)-1:#it's my tail!
                    self.grid[segment['y']][segment['x']] = [0, 1, 0, 0, 0]
                else:#just bodycoord
                    self.grid[segment['y']][segment['x']] = [0, 0, 1, 0, 0]
            else:#it's opp
                if i==len(snake_body)-1:#its opponents tail
                    self.grid[segment['y']][segment['x']] = [0, 1, 0, 0, 0]
                else:#it's just bodycoord
                    self.grid[segment['y']][segment['x']] = [0, 0, 1, 0, 0]
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
                #print("starvation")
                self.kill_snake(snakeindex)
            elif (thissnake.head['x']<0 or thissnake.head['x']>=self.width or thissnake.head['y']<0 or thissnake.head['y']>=self.height):
                #print("oub")
                self.kill_snake(snakeindex)
            if self.snakes[snakeindex]!=None and not self.snakes[snakeindex].instartingspot():
                #print("collide with self")
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
        for snake in self.snakes:
            snake.newturn()
        determinedreward=0
        myindex = self.selfindex
        dideat = self.move_snake(myindex, myaction) #determine if eated
        if dideat!=None:
            determinedreward+=6.0
        #self.update_board()
        #self.printself()
        #print("this is the board after only you made the move")
        model = PPO.load("snakemodelppo_dc1.1.5")
        movelist = ['up', 'down', 'left', 'right']
        for i in range(len(self.snakes)):
            if i!=myindex and self.snakes[i]!=None:
                oppsafemoves = self.snakes[i].getsafemoves(self.snakes)
                safemovesnonone = []
                for thing in oppsafemoves:
                    if thing!=None:
                        safemovesnonone.append(thing)
                oppaction, _states = model.predict(numpy.array(self.returngrid()), deterministic=False)
                
                if (oppsafemoves[oppaction] == None):#unsafe
                    if (len(safemovesnonone)>0):
                        saferesort = random.choice(safemovesnonone)
                        if self.debug:
                            print("opp chose:", saferesort, "(saferesort)")
                        self.move_snake(i, saferesort)
                    else:
                        if self.debug:
                            print("opp is screwed, chose up")
                        self.move_snake(i, 'up')
                        #this snake is screwed
                else:#safe
                    if self.debug:
                        print("ai chose", movelist[oppaction], "seems safe.")
                    self.move_snake(i, movelist[oppaction])
        for i in range(len(self.snakes)):
            self.dead_check(i)
        self.update_board()
        # get open squares
        #min food on board must be 1
        #15% chance to spawn food otherwise
        openspaces = []
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if self.grid[y][x] == [0, 0, 0, 0, 0]:
                    openspaces.append([x, y])
        if (len(self.foods)==0):
            chosenopenspace = random.choice(openspaces)
            self.add_food({
                'x':chosenopenspace[0],
                'y':chosenopenspace[1],
            })
            #self.update_board()
        while (random.random()<0.15):
            openspaces = []
            for y in range(len(self.grid)):
                for x in range(len(self.grid[y])):
                    if self.grid[y][x] == [0, 0, 0, 0, 0]:
                        openspaces.append([x, y])
            try:
                chosenopenspace = random.choice(openspaces)
                self.add_food({
                    'x':chosenopenspace[0],
                    'y':chosenopenspace[1],
                })
            except:
                self.printself()
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
                        print('T', end='')
                    elif type==2:
                        print('B', end='')
                    elif type==3:
                        print('O', end='')
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
        if len(self.snakes)==1:
            #this means it's a solo run
            alldead=False
        return alldead
    def returngrid(self):
        return self.grid
    def rotate_2d_array_clockwise(self, matrix):
        return [list(row) for row in zip(*matrix[::-1])]
    def aligngridtoup(self, snakeindex, grid):
        targetsnake = self.snakes[snakeindex]
        directions = [#add to head and compare to neck
            [0, -1],#heading upward
            [1, 0],#heading leftward
            [0, 1],#heading downward
            [-1, 0],#heading rightward
        ]
        newgrid = deepcopy(grid)
        rotationnum = [0, 1, 2, 3]
        directionindex = 0
        for i in range(4):
            if targetsnake.body[0]['x']+directions[i][0] == targetsnake.body[1]['x'] and targetsnake.body[0]['y']+directions[i][1] == targetsnake.body[1]['y']:
                directionindex=i
        for i in range(directionindex):
            newgrid = deepcopy(self.rotate_2d_array_clockwise(newgrid))
        return newgrid
    def returngridjustfood(self):
        foodgrid = []
        horiz_border = []
        for i in range((self.width)+2):
            horiz_border.append(0)
        foodgrid.append(deepcopy(horiz_border))
        for y in range((self.height)):
            thisrow_food = []
            thisrow_food.append(0)
            for x in range(self.width):
                if self.grid[y][x] == [1, 0, 0, 0, 0]:
                    thisrow_food.append(2)
                else:
                    thisrow_food.append(1)
            thisrow_food.append(0)
            foodgrid.append(thisrow_food)
        foodgrid.append(deepcopy(horiz_border))
        if self.snakes[self.selfindex]!=None:
            foodgrid = deepcopy(self.aligngridtoup(self.selfindex, foodgrid))
        return foodgrid
    
    def returngridjustself(self):
        selfgrid = []
        horiz_border = []
        default_row = []
        for i in range((self.width)+2):
            horiz_border.append(0)
            if i==0 or i==self.width+1:
                default_row.append(0)
            else:
                default_row.append(1)
        selfgrid.append(deepcopy(horiz_border))
        for i in range(self.height):
            selfgrid.append(deepcopy(default_row))
        selfgrid.append(deepcopy(horiz_border))
        if (self.snakes[self.selfindex]!=None):
            mybody = self.snakes[self.selfindex].body
            #print('mybodylen', len(mybody))
            for i in range(len(mybody)-1, -1, -1):#head=3, tail=2, body=1
                converted_bodycoord = [mybody[i]['x']+1, mybody[i]['y']+1]#plus one because im adding borders
                #print(converted_bodycoord[0], "x", converted_bodycoord[1], 'y')
                #print(converted_bodycoord, "has number", i+2)
                selfgrid[converted_bodycoord[1]][converted_bodycoord[0]] = (i+1)+1
            selfgrid = deepcopy(self.aligngridtoup(self.selfindex, selfgrid))
            return selfgrid
        else:
            return selfgrid
    
    def returngridjustopps(self, justsmaller=False, justdanger=False):
        oppgrid = []
        horiz_border = []
        default_row = []
        for i in range((self.width)+2):
            horiz_border.append(0)
            if i==0 or i==self.width+1:
                default_row.append(0)
            else:
                default_row.append(1)
        oppgrid.append(deepcopy(horiz_border))
        for i in range(self.height):
            oppgrid.append(deepcopy(default_row))
        oppgrid.append(deepcopy(horiz_border))
        if self.snakes[self.selfindex]!=None:
            for i in range(len(self.snakes)):
                if i!=self.selfindex and self.snakes[i]!=None:
                    addsnake=False
                    if (justsmaller and len(self.snakes[i].body)<len(self.snakes[self.selfindex].body)):
                        addsnake=True
                    elif (justdanger and len(self.snakes[i].body)>=len(self.snakes[self.selfindex].body)):
                        addsnake=True
                    elif (not justsmaller and not justdanger):
                        addsnake=True
                    if addsnake:
                        thisoppbody = self.snakes[i].body
                        for j in range(len(thisoppbody)-1, -1, -1):#head=3, tail=2, body=1
                            converted_bodycoord = [thisoppbody[j]['x']+1, thisoppbody[j]['y']+1]#plus one because im adding borders
                            oppgrid[converted_bodycoord[1]][converted_bodycoord[0]] = (j+1)+1
            if self.snakes[self.selfindex]!=None:
                oppgrid = deepcopy(self.aligngridtoup(self.selfindex, oppgrid))
        return oppgrid
    def returngrideverysnake(self):
        oppgrid = []
        horiz_border = []
        default_row = []
        for i in range((self.width)+2):
            horiz_border.append(0)
            if i==0 or i==self.width+1:
                default_row.append(0)
            else:
                default_row.append(1)
        oppgrid.append(deepcopy(horiz_border))
        for i in range(self.height):
            oppgrid.append(deepcopy(default_row))
        oppgrid.append(deepcopy(horiz_border))
        if self.snakes[self.selfindex]!=None:
            for i in range(len(self.snakes)):
                if self.snakes[i]!=None:
                    thisoppbody = self.snakes[i].body
                    for j in range(len(thisoppbody)-1, -1, -1):#head=3, tail=2, body=1
                        converted_bodycoord = [thisoppbody[j]['x']+1, thisoppbody[j]['y']+1]#plus one because im adding borders
                        oppgrid[converted_bodycoord[1]][converted_bodycoord[0]] = (j+1)+1
            if self.snakes[self.selfindex]!=None:
                oppgrid = deepcopy(self.aligngridtoup(self.selfindex, oppgrid))
        return oppgrid
    def printself3channel(self, grid1, grid2, grid3):
        # Example 13x13 grids as normal lists
        # Print the grids side by side
        for row1, row2, row3 in zip(grid1, grid2, grid3):
            print(" ".join(f"{val:1}" for val in row1), "|", " ".join(f"{val:1}" for val in row2), "|", " ".join(f"{val:1}" for val in row3))
    

    def return6channel(self, justrender=False):
        #TODO
        headgrid = []
        horiz_border = []
        default_row = []
        for i in range((self.width)+2):
            horiz_border.append(0)
            if i==0 or i==self.width+1:
                default_row.append(0)
            else:
                default_row.append(1)
        headgrid.append(deepcopy(horiz_border))
        for i in range(self.height):
            headgrid.append(deepcopy(default_row))
        headgrid.append(deepcopy(horiz_border))
        if self.snakes[self.selfindex]!=None:
            headgrid[self.snakes[self.selfindex].body[0]['y']][self.snakes[self.selfindex].body[0]['x']]=2
            headgrid = deepcopy(self.aligngridtoup(self.selfindex, headgrid))
        selfgrid = self.returngridjustself()#already aligned to up
        allsnakesgrid = self.returngrideverysnake()#already aligned
        if justrender:
            self.printself3channel(headgrid, selfgrid, allsnakesgrid)
            print()
        foodgrid = self.returngridjustfood()#already aligned
        dangersnakesgrid = self.returngridjustopps(False, True)
        victimsnakesgrid = self.returngridjustopps(True, False)
        if justrender:
            self.printself3channel(foodgrid, dangersnakesgrid, victimsnakesgrid)
        if not justrender:
            return numpy.stack([headgrid, selfgrid, allsnakesgrid, foodgrid, dangersnakesgrid, victimsnakesgrid], axis=0)
        #grid with just your head
        # your body, segments numbered
        # all snake bodies, segments numbered
        # foodgrid
        # all snake bodies greater than or equal to you, segments numbered
        # all snake bodies smaller than you, segments numbered