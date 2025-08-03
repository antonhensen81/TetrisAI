import pygame
import sys
from game import TetrisGame
from controls import Controls

class TetrisRenderer:
    def __init__(self, game):
        self.game = game
        self.BLOCK_SIZE = game.BLOCK_SIZE
        self.BOARD_WIDTH = game.BOARD_WIDTH * self.BLOCK_SIZE
        self.BOARD_HEIGHT = game.BOARD_HEIGHT * self.BLOCK_SIZE
        self.SIDEBAR_WIDTH = 200
        self.WINDOW_WIDTH = self.BOARD_WIDTH + self.SIDEBAR_WIDTH
        self.WINDOW_HEIGHT = self.BOARD_HEIGHT
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.GHOST_ALPHA = 100
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def draw_block(self, x, y, color, alpha=255):
        rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE, 
                          self.BLOCK_SIZE, self.BLOCK_SIZE)
        
        if alpha < 255:
            surf = pygame.Surface((self.BLOCK_SIZE, self.BLOCK_SIZE))
            surf.set_alpha(alpha)
            surf.fill(color)
            self.screen.blit(surf, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.WHITE, rect, 1)
    
    def draw_board(self):
        for y in range(self.game.BOARD_HEIGHT):
            for x in range(self.game.BOARD_WIDTH):
                if self.game.board[y][x] != 0:
                    color = self.game.board_colors[y][x]
                    self.draw_block(x, y, color)
                else:
                    rect = pygame.Rect(x * self.BLOCK_SIZE, y * self.BLOCK_SIZE,
                                     self.BLOCK_SIZE, self.BLOCK_SIZE)
                    pygame.draw.rect(self.screen, self.DARK_GRAY, rect, 1)
    
    def draw_piece(self, piece, alpha=255):
        for x, y in piece.get_blocks():
            if 0 <= x < self.game.BOARD_WIDTH and y >= 0:
                self.draw_block(x, y, piece.color, alpha)
    
    def draw_ghost_piece(self):
        ghost = self.game.get_ghost_piece()
        self.draw_piece(ghost, self.GHOST_ALPHA)
    
    def draw_next_piece(self):
        next_x = self.BOARD_WIDTH + 20
        next_y = 50
        
        text = self.font.render("Next:", True, self.WHITE)
        self.screen.blit(text, (next_x, next_y - 30))
        
        shape = self.game.next_piece.get_shape()
        for row_idx, row in enumerate(shape):
            for col_idx, cell in enumerate(row):
                if cell == '#':
                    x = next_x + col_idx * 20
                    y = next_y + row_idx * 20
                    rect = pygame.Rect(x, y, 20, 20)
                    pygame.draw.rect(self.screen, self.game.next_piece.color, rect)
                    pygame.draw.rect(self.screen, self.WHITE, rect, 1)
    
    def draw_score(self):
        score_x = self.BOARD_WIDTH + 20
        score_y = 150
        
        score_text = self.font.render(f"Score: {self.game.score}", True, self.WHITE)
        self.screen.blit(score_text, (score_x, score_y))
        
        lines_text = self.font.render(f"Lines: {self.game.lines_cleared}", True, self.WHITE)
        self.screen.blit(lines_text, (score_x, score_y + 40))
        
        level_text = self.font.render(f"Level: {self.game.level}", True, self.WHITE)
        self.screen.blit(level_text, (score_x, score_y + 80))
    
    def draw_controls(self):
        controls_x = self.BOARD_WIDTH + 20
        controls_y = 300
        
        controls_text = [
            "Controls:",
            "A/← - Move Left",
            "D/→ - Move Right", 
            "S/↓ - Soft Drop",
            "W/↑/Space - Rotate",
            "Z - Hard Drop",
            "P - Pause",
            "ESC - Quit"
        ]
        
        for i, text in enumerate(controls_text):
            if i == 0:
                rendered = self.font.render(text, True, self.WHITE)
            else:
                rendered = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(rendered, (controls_x, controls_y + i * 25))
    
    def draw_game_over(self):
        if self.game.game_over:
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.font.render("GAME OVER", True, self.WHITE)
            restart_text = self.small_font.render("Press R to restart", True, self.WHITE)
            
            text_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
            restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 40))
            
            self.screen.blit(game_over_text, text_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def draw_paused(self):
        if self.game.paused:
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            paused_text = self.font.render("PAUSED", True, self.WHITE)
            text_rect = paused_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
            self.screen.blit(paused_text, text_rect)
    
    def render(self):
        self.screen.fill(self.BLACK)
        
        self.draw_board()
        
        if not self.game.game_over and not self.game.paused:
            self.draw_ghost_piece()
            self.draw_piece(self.game.current_piece)
        
        self.draw_next_piece()
        self.draw_score()
        self.draw_controls()
        self.draw_game_over()
        self.draw_paused()
        
        pygame.display.flip()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    renderer = TetrisRenderer(game)
    controls = Controls()
    
    move_timer = 0
    move_delay = 100
    
    running = True
    while running:
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game.game_over:
                    game.reset_game()
                else:
                    controls.handle_event(event)
            else:
                controls.handle_event(event)
        
        if controls.is_quit_pressed():
            running = False
        
        if not game.game_over:
            if controls.is_pause_pressed():
                game.toggle_pause()
            
            if not game.paused:
                move_timer += dt
                
                if controls.is_left_pressed() and move_timer >= move_delay:
                    game.move_piece(-1, 0)
                    move_timer = 0
                elif controls.is_right_pressed() and move_timer >= move_delay:
                    game.move_piece(1, 0)
                    move_timer = 0
                elif controls.is_down_pressed() and move_timer >= move_delay // 2:
                    if game.move_piece(0, 1):
                        game.score += 1
                    move_timer = 0
                
                if controls.is_rotate_pressed():
                    game.rotate_piece()
                
                if controls.is_hard_drop_pressed():
                    game.hard_drop()
                
                game.update(dt)
        
        renderer.render()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()