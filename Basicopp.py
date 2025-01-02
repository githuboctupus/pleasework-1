import random

class GridBasedOpponent:
    def __init__(self):
        self.directions = ['up', 'down', 'left', 'right']
    
    def get_move(self, grid, my_head):

        """
        Takes in the 11x11 grid (with each cell being a [isfood, isoppbody, isopphead, ismybody, ismyhead]) 
        and your snake's head position.
        
        Returns a move: 'up', 'down', 'left', 'right'.
        """
        
        # Identify the potential directions from the current head position
        possible_moves = self.get_possible_moves(my_head)
        
        # First, try to avoid danger (e.g., opponent head and body)
        safe_moves = self.avoid_danger(possible_moves, grid, my_head)
        
        if safe_moves:
            # If there are safe moves, choose one of them
            return random.choice(safe_moves)
        
        # If no safe moves, go towards food (greedy strategy)
        food_moves = self.move_towards_food(possible_moves, grid, my_head)
        
        if food_moves:
            return random.choice(food_moves)
        
        # Otherwise, pick a random move (fallback)
        return random.choice(possible_moves)
    
    def get_possible_moves(self, head):
        """
        Given the current head position, return the list of possible moves:
        - 'up' if moving up is valid
        - 'down' if moving down is valid
        - 'left' if moving left is valid
        - 'right' if moving right is valid
        """
        x, y = head
        possible_moves = []
        
        # Check bounds and directions
        if x > 0: possible_moves.append('left')
        if x < 10: possible_moves.append('right')
        if y > 0: possible_moves.append('up')
        if y < 10: possible_moves.append('down')
        
        return possible_moves
    
    def avoid_danger(self, possible_moves, grid, my_head):
        """
        Avoid moves that lead to danger (opponent's head, body, or walls).
        """
        safe_moves = []
        x, y = my_head
        
        for move in possible_moves:
            if move == 'up':
                next_cell = (x, y + 1)
            elif move == 'down':
                next_cell = (x, y - 1)
            elif move == 'left':
                next_cell = (x - 1, y)
            elif move == 'right':
                next_cell = (x + 1, y)
            
            # Check if next cell contains danger (opponent body, head, or out of bounds)
            if self.is_safe_cell(next_cell, grid):
                safe_moves.append(move)
        
        return safe_moves
    
    def is_safe_cell(self, next_cell, grid):
        """
        Check if the next cell is safe to move to. It should not contain an opponent's head or body.
        """
        x, y = next_cell
        if grid[y][x][2] == 1:  # Opponent's head
            return False
        if grid[y][x][1] == 1:  # Opponent's body
            return False
        if grid[y][x][3] == 1:  # Your own body
            return False
        return True
    
    def move_towards_food(self, possible_moves, grid, my_head):
        """
        Move towards food if it's nearby.
        """
        x, y = my_head
        food_moves = []
        
        for move in possible_moves:
            if move == 'up':
                next_cell = (x, y - 1)
            elif move == 'down':
                next_cell = (x, y + 1)
            elif move == 'left':
                next_cell = (x - 1, y)
            elif move == 'right':
                next_cell = (x + 1, y)
            
            # If the next cell contains food, prioritize this move
            if self.is_food_cell(next_cell, grid):
                food_moves.append(move)
        
        return food_moves
    
    def is_food_cell(self, next_cell, grid):
        """
        Check if the next cell contains food.
        """
        x, y = next_cell
        if grid[y][x][0] == 1:  # Food
            return True
        return False