import pygame
import random
from tetromino import Tetromino

class TetrisGame:
    def __init__(self):
        self.BOARD_WIDTH = 10
        self.BOARD_HEIGHT = 20
        self.BLOCK_SIZE = 30
        
        self.board = [[0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.board_colors = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        
        self.fall_time = 0
        self.fall_speed = 500
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        
        self.game_over = False
        self.paused = False
        
    def is_valid_position(self, piece, dx=0, dy=0, rotation=None):
        if rotation is not None:
            test_piece = piece.copy()
            test_piece.rotation = rotation
            test_piece.x += dx
            test_piece.y += dy
            blocks = test_piece.get_blocks()
        else:
            blocks = []
            for x, y in piece.get_blocks():
                blocks.append((x + dx, y + dy))
        
        for x, y in blocks:
            if x < 0 or x >= self.BOARD_WIDTH or y >= self.BOARD_HEIGHT:
                return False
            if y >= 0 and self.board[y][x] != 0:
                return False
        return True
    
    def place_piece(self, piece):
        for x, y in piece.get_blocks():
            if y >= 0:
                self.board[y][x] = 1
                self.board_colors[y][x] = piece.color
        
        lines_to_clear = self.get_complete_lines()
        if lines_to_clear:
            self.clear_lines(lines_to_clear)
            self.update_score(len(lines_to_clear))
        
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        if not self.is_valid_position(self.current_piece):
            self.game_over = True
    
    def get_complete_lines(self):
        complete_lines = []
        for y in range(self.BOARD_HEIGHT):
            if all(self.board[y][x] != 0 for x in range(self.BOARD_WIDTH)):
                complete_lines.append(y)
        return complete_lines
    
    def clear_lines(self, lines_to_clear):
        for line in sorted(lines_to_clear, reverse=True):
            del self.board[line]
            del self.board_colors[line]
            self.board.insert(0, [0 for _ in range(self.BOARD_WIDTH)])
            self.board_colors.insert(0, [None for _ in range(self.BOARD_WIDTH)])
        
        self.lines_cleared += len(lines_to_clear)
        self.level = self.lines_cleared // 10 + 1
        self.fall_speed = max(50, 500 - (self.level - 1) * 50)
    
    def update_score(self, lines_cleared):
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += points.get(lines_cleared, 0) * self.level
    
    def move_piece(self, dx, dy):
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.move(dx, dy)
            return True
        return False
    
    def rotate_piece(self):
        next_rotation = (self.current_piece.rotation + 1) % len(self.current_piece.shapes)
        if self.is_valid_position(self.current_piece, rotation=next_rotation):
            self.current_piece.rotate()
            return True
        return False
    
    def hard_drop(self):
        while self.move_piece(0, 1):
            self.score += 2
        self.place_piece(self.current_piece)
    
    def update(self, dt):
        if self.game_over or self.paused:
            return
        
        self.fall_time += dt
        if self.fall_time >= self.fall_speed:
            if not self.move_piece(0, 1):
                self.place_piece(self.current_piece)
            self.fall_time = 0
    
    def toggle_pause(self):
        self.paused = not self.paused
    
    def reset_game(self):
        self.board = [[0 for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.board_colors = [[None for _ in range(self.BOARD_WIDTH)] for _ in range(self.BOARD_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.score = 0
        self.lines_cleared = 0
        self.level = 1
        self.fall_speed = 500
        self.fall_time = 0
        self.game_over = False
        self.paused = False
    
    def get_ghost_piece(self):
        ghost = self.current_piece.copy()
        while self.is_valid_position(ghost, 0, 1):
            ghost.move(0, 1)
        return ghost