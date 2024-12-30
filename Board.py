import Snake
class Board:
    #board is in reverse height order visually
    def __init__(self, width, height):
        self.snakes = [] #list of Snake objects
        self.foods = [] #dict form
        self.width = width
        self.height = height
        self.grid = [[None for _ in range(width)] for _ in range(height)]  # None represents empty space
    def place_food(self, food_list):
        for food in food_list:
            self.foods.append(food)#dict form
            self.grid[food['y']][food['x']] = 'food'
    def add_food(self, newfood):
        self.foods.append(newfood)#dict form
        self.grid[newfood['y']][newfood['x']] = 'food'
    def place_snake(self, snakeobject):
        snake_body=snakeobject.body
        self.snakes.append(snakeobject)
        for segment in snake_body:
            self.grid[segment['y']][segment['x']] = 'snake'
    def move_snake(self, snakeindex, direction):
        selectedsnake = self.snakes[snakeindex]
        dideat = selectedsnake.move(direction)
        if dideat!=None:
            for i in range(len(self.foods)):
                if (self.foods[i]['x'] == dideat['x'] and self.foods[i]['y'] == dideat['y']):
                    del self.foods[i]
    def update_board(self):
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        for snake in self.snakes:
            for bodycoord_dict in snake.get_body():
                self.grid[bodycoord_dict['y']][bodycoord_dict['x']] = 'snake'
        self.place_food(self.foods)
    def get_cell(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return 'wall'  # Represents out-of-bounds as a wall
    def printself(self):
        for i in range(self.height):
            print(self.grid[self.height-i])