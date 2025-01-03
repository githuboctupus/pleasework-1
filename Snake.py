import json
class Snake:
    def __init__(self, gamedata, myindex, health=100):
        self.id = id
        self.gamedata=gamedata
        self.mydata = gamedata['board']['snakes'][myindex]
        self.name = self.mydata['name']
        self.body = self.mydata['body'] #list of coords in dict form
        self.health = health
        self.head = self.body[0]  # The head is the first element of the body dict form
        self.length = len(self.body)
        self.hasmoved = False

    def move(self, direction, food_list):
        head_x = self.head['x']
        head_y = self.head['y']
        new_head = {'x': head_x, 'y': head_y + 1}#dummy value
        if direction == 'up':
            new_head = {'x': head_x, 'y': head_y + 1}
        elif direction == 'down':
            new_head = {'x': head_x, 'y': head_y - 1}
        elif direction == 'left':
            new_head = {'x': head_x-1, 'y': head_y}
        elif direction == 'right':
            new_head = {'x': head_x+1, 'y': head_y}
        # Update the body (new head added, last segment removed)
        self.body = [new_head] + self.body[:-1]
        self.head = new_head
        ate=None
        for foodcoord_dict in food_list:
            if (new_head['x']==foodcoord_dict['x'] and new_head['y'] == foodcoord_dict['y']):
                ate=foodcoord_dict
                self.body.append(self.body[len(self.body)-1])
        self.length = len(self.body)
        self.hasmoved = True
        return ate
    def newturn(self):
        self.hasmoved=False
    def get_body(self):
        return self.body #dict form
    def instartingspot(self):
        instartingspot=True
        if len(self.body)!=3:
            return False
        currenthead = self.body[0]
        for i in range(len(self.body)):
            if currenthead['x']==self.body[i]['x'] and currenthead['y'] == self.body[i]['y']:
                pass
            else:
                instartingspot=False
        if instartingspot:
            print("this shit worked")
        return instartingspot
    def getsafemoves(self, allsnakes):#make the opps intelligent (more than 1 IQ)
        currenthead = [self.head['x'], self.head['y']]
        movechoices = [
            [currenthead[0], currenthead[1]+1],#up
            [currenthead[0], currenthead[1]-1],#down
            [currenthead[0]-1, currenthead[1]],#left
            [currenthead[0]+1, currenthead[1]],#right
        ]
        for i in range(4):
            if movechoices[i][0]<0 or movechoices[i][0]>=self.gamedata['board']['width'] or movechoices[i][1]<0 or movechoices[i][1]>=self.gamedata['board']['height']:
                #print("move", i, "is oub")
                movechoices[i]=None
        for m in range(4):
            if movechoices[m]!=None:
                for snake in allsnakes:
                    opphasmoved = 0
                    if snake.hasmoved:
                        opphasmoved=1
                    for i in range(len(snake.body)-opphasmoved):
                        if (movechoices[m]!=None):
                            if movechoices[m][0]==snake.body[i]['x'] and movechoices[m][1]==snake.body[i]['y']:
                                #print("move", m, "is in a body")
                                movechoices[m]=None
                        #else:
                            #print("move", m, "with coord", movechoices[m], "isn't in bodycoord", snake.body[i])
        returnme = ['up', 'down', 'left', 'right']
        for i in range(4):
            if movechoices[i]==None:
                returnme[i]=None
        return returnme