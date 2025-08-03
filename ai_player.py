import copy
from tetromino import Tetromino

class TetrisAI:
    def __init__(self):
        self.hole_weight = -5.0
        self.landing_height_weight = -1.0
        self.lines_cleared_weight = 10.0
        self.bumpiness_weight = -2.0
        
    def set_weights(self, hole_weight, landing_height_weight, lines_cleared_weight=10.0, bumpiness_weight=-2.0):
        self.hole_weight = hole_weight
        self.landing_height_weight = landing_height_weight
        self.lines_cleared_weight = lines_cleared_weight
        self.bumpiness_weight = bumpiness_weight
    
    def count_holes(self, board):
        holes = 0
        height = len(board)
        width = len(board[0])
        
        for col in range(width):
            found_filled = False
            for row in range(height):
                if board[row][col] != 0:
                    found_filled = True
                elif found_filled and board[row][col] == 0:
                    holes += 1
        return holes
    
    def get_landing_height(self, piece):
        return piece.y
    
    def get_column_heights(self, board):
        heights = []
        width = len(board[0])
        height = len(board)
        
        for col in range(width):
            col_height = 0
            for row in range(height):
                if board[row][col] != 0:
                    col_height = height - row
                    break
            heights.append(col_height)
        return heights
    
    def calculate_bumpiness(self, board):
        heights = self.get_column_heights(board)
        bumpiness = 0
        for i in range(len(heights) - 1):
            bumpiness += abs(heights[i] - heights[i + 1])
        return bumpiness
    
    def count_lines_cleared(self, board):
        lines_cleared = 0
        for row in board:
            if all(cell != 0 for cell in row):
                lines_cleared += 1
        return lines_cleared
    
    def simulate_placement(self, game, piece, rotation, x):
        test_game = copy.deepcopy(game)
        test_piece = piece.copy()
        test_piece.rotation = rotation
        test_piece.x = x
        test_piece.y = 0
        
        while test_game.is_valid_position(test_piece, 0, 1):
            test_piece.move(0, 1)
        
        if not test_game.is_valid_position(test_piece):
            return None
        
        for block_x, block_y in test_piece.get_blocks():
            if block_y >= 0:
                test_game.board[block_y][block_x] = 1
        
        landing_height = test_piece.y
        holes = self.count_holes(test_game.board)
        lines_cleared = self.count_lines_cleared(test_game.board)
        bumpiness = self.calculate_bumpiness(test_game.board)
        
        score = (self.hole_weight * holes + 
                self.landing_height_weight * landing_height +
                self.lines_cleared_weight * lines_cleared +
                self.bumpiness_weight * bumpiness)
        
        return {
            'score': score,
            'rotation': rotation,
            'x': x,
            'landing_height': landing_height,
            'holes': holes,
            'lines_cleared': lines_cleared,
            'bumpiness': bumpiness
        }
    
    def get_best_move(self, game):
        best_move = None
        best_score = float('-inf')
        
        current_piece = game.current_piece
        
        for rotation in range(len(current_piece.shapes)):
            for x in range(-2, game.BOARD_WIDTH + 2):
                result = self.simulate_placement(game, current_piece, rotation, x)
                if result and result['score'] > best_score:
                    best_score = result['score']
                    best_move = result
        
        return best_move
    
    def get_move_sequence(self, game, target_rotation, target_x):
        moves = []
        current_rotation = game.current_piece.rotation
        current_x = game.current_piece.x
        
        rotation_diff = (target_rotation - current_rotation) % len(game.current_piece.shapes)
        for _ in range(rotation_diff):
            moves.append('rotate')
        
        x_diff = target_x - current_x
        if x_diff > 0:
            for _ in range(x_diff):
                moves.append('right')
        elif x_diff < 0:
            for _ in range(abs(x_diff)):
                moves.append('left')
        
        moves.append('hard_drop')
        return moves