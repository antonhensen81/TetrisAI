import random

class Tetromino:
    SHAPES = {
        'I': [
            ['.....',
             '..#..',
             '..#..',
             '..#..',
             '..#..'],
            ['.....',
             '.....',
             '####.',
             '.....',
             '.....']
        ],
        'O': [
            ['.....',
             '.....',
             '.##..',
             '.##..',
             '.....']
        ],
        'T': [
            ['.....',
             '.....',
             '.#...',
             '###..',
             '.....'],
            ['.....',
             '.....',
             '.#...',
             '.##..',
             '.#...'],
            ['.....',
             '.....',
             '.....',
             '###..',
             '.#...'],
            ['.....',
             '.....',
             '.#...',
             '##...',
             '.#...']
        ],
        'S': [
            ['.....',
             '.....',
             '.##..',
             '##...',
             '.....'],
            ['.....',
             '.#...',
             '.##..',
             '..#..',
             '.....']
        ],
        'Z': [
            ['.....',
             '.....',
             '##...',
             '.##..',
             '.....'],
            ['.....',
             '..#..',
             '.##..',
             '.#...',
             '.....']
        ],
        'J': [
            ['.....',
             '.#...',
             '.#...',
             '##...',
             '.....'],
            ['.....',
             '.....',
             '#....',
             '###..',
             '.....'],
            ['.....',
             '.##..',
             '.#...',
             '.#...',
             '.....'],
            ['.....',
             '.....',
             '###..',
             '..#..',
             '.....']
        ],
        'L': [
            ['.....',
             '..#..',
             '..#..',
             '.##..',
             '.....'],
            ['.....',
             '.....',
             '###..',
             '#....',
             '.....'],
            ['.....',
             '##...',
             '.#...',
             '.#...',
             '.....'],
            ['.....',
             '.....',
             '..#..',
             '###..',
             '.....']
        ]
    }
    
    COLORS = {
        'I': (0, 255, 255),    # Cyan
        'O': (255, 255, 0),    # Yellow
        'T': (128, 0, 128),    # Purple
        'S': (0, 255, 0),      # Green
        'Z': (255, 0, 0),      # Red
        'J': (0, 0, 255),      # Blue
        'L': (255, 165, 0)     # Orange
    }
    
    def __init__(self, shape_type=None):
        if shape_type is None:
            self.shape_type = random.choice(list(self.SHAPES.keys()))
        else:
            self.shape_type = shape_type
            
        self.shapes = self.SHAPES[self.shape_type]
        self.color = self.COLORS[self.shape_type]
        self.rotation = 0
        self.x = 3
        self.y = 0
        
    def get_shape(self):
        return self.shapes[self.rotation]
    
    def get_rotated_shape(self):
        next_rotation = (self.rotation + 1) % len(self.shapes)
        return self.shapes[next_rotation]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes)
    
    def get_blocks(self):
        blocks = []
        shape = self.get_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks
    
    def get_rotated_blocks(self):
        blocks = []
        shape = self.get_rotated_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    blocks.append((self.x + col_idx, self.y + row_idx))
        return blocks
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def copy(self):
        new_piece = Tetromino(self.shape_type)
        new_piece.rotation = self.rotation
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece