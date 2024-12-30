class Snake:
    def __init__(self, gamedata, myindex, health=100):
        self.id = id
        self.mydata = gamedata['board']['snakes'][myindex]
        self.name = mydata['name']
        self.body = body #dict form
        self.health = health
        self.head = body[0]  # The head is the first element of the body dict form
        self.length = len(body)

    def move(self, direction, food_list):
        head_x = self.head['x']
        head_y = self.head['y']
        if direction == 'up':
            new_head = (head_x, head_y + 1)
        elif direction == 'down':
            new_head = (head_x, head_y - 1)
        elif direction == 'left':
            new_head = (head_x - 1, head_y)
        elif direction == 'right':
            new_head = (head_x + 1, head_y)
        else:
            return
        # Update the body (new head added, last segment removed)
        self.body = [new_head] + self.body[:-1]
        self.head = new_head
        ate=None
        for foodcoord_dict in food_list:
            if (new_head['x']==foodcoord_dict['x'] and new_head['y'] == foodcoord_dict['y']):
                ate=foodcoord_dict
                self.body.append(self.body[len(self.body)-1])
        self.length = len(self.body)
        return ate
    def get_body(self):
        return self.body #dict form