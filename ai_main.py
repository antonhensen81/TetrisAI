import pygame
import sys
from game import TetrisGame
from ai_controls import AIControls

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, initial_val, label):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.val = initial_val
        self.label = label
        self.dragging = False
        
        self.slider_rect = pygame.Rect(x, y, width, height)
        self.handle_rect = pygame.Rect(x + (initial_val - min_val) / (max_val - min_val) * width - 5, y - 2, 10, height + 4)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.handle_rect.collidepoint(event.pos):
                self.dragging = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            rel_x = event.pos[0] - self.slider_rect.x
            rel_x = max(0, min(rel_x, self.slider_rect.width))
            self.val = self.min_val + (rel_x / self.slider_rect.width) * (self.max_val - self.min_val)
            self.handle_rect.centerx = self.slider_rect.x + rel_x
    
    def draw(self, screen, font):
        pygame.draw.rect(screen, (100, 100, 100), self.slider_rect)
        pygame.draw.rect(screen, (200, 200, 200), self.handle_rect)
        
        label_text = font.render(f"{self.label}: {self.val:.1f}", True, (255, 255, 255))
        screen.blit(label_text, (self.slider_rect.x, self.slider_rect.y - 25))

class AITetrisRenderer:
    def __init__(self, game):
        self.game = game
        self.BLOCK_SIZE = game.BLOCK_SIZE
        self.BOARD_WIDTH = game.BOARD_WIDTH * self.BLOCK_SIZE
        self.BOARD_HEIGHT = game.BOARD_HEIGHT * self.BLOCK_SIZE
        self.SIDEBAR_WIDTH = 300
        self.CONTROL_PANEL_WIDTH = 250
        self.WINDOW_WIDTH = self.BOARD_WIDTH + self.SIDEBAR_WIDTH + self.CONTROL_PANEL_WIDTH
        self.WINDOW_HEIGHT = self.BOARD_HEIGHT
        
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.DARK_GRAY = (64, 64, 64)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.GHOST_ALPHA = 100
        
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("AI Tetris")
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 32)
        
        control_x = self.BOARD_WIDTH + self.SIDEBAR_WIDTH + 20
        self.sliders = [
            Slider(control_x, 50, 180, 20, -10, 10, -5, "Hole Weight"),
            Slider(control_x, 120, 180, 20, -10, 10, -1, "Landing Height Weight"),
            Slider(control_x, 190, 180, 20, -10, 10, 10, "Lines Cleared Weight"),
            Slider(control_x, 260, 180, 20, -10, 10, -2, "Bumpiness Weight")
        ]
        
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
        self.screen.blit(lines_text, (score_x, score_y + 30))
        
        level_text = self.font.render(f"Level: {self.game.level}", True, self.WHITE)
        self.screen.blit(level_text, (score_x, score_y + 60))
    
    def draw_ai_info(self, ai_controls):
        info_x = self.BOARD_WIDTH + 20
        info_y = 280
        
        title = self.font.render("AI Analysis:", True, self.WHITE)
        self.screen.blit(title, (info_x, info_y))
        
        evaluation = ai_controls.get_current_evaluation()
        if evaluation:
            y_offset = info_y + 30
            
            score_text = self.small_font.render(f"Move Score: {evaluation['score']:.1f}", True, self.WHITE)
            self.screen.blit(score_text, (info_x, y_offset))
            
            holes_color = self.RED if evaluation['holes'] > 5 else self.WHITE
            holes_text = self.small_font.render(f"Holes: {evaluation['holes']}", True, holes_color)
            self.screen.blit(holes_text, (info_x, y_offset + 20))
            
            height_color = self.RED if evaluation['landing_height'] > 15 else self.WHITE
            height_text = self.small_font.render(f"Landing Height: {evaluation['landing_height']}", True, height_color)
            self.screen.blit(height_text, (info_x, y_offset + 40))
            
            lines_color = self.GREEN if evaluation['lines_cleared'] > 0 else self.WHITE
            lines_text = self.small_font.render(f"Lines Cleared: {evaluation['lines_cleared']}", True, lines_color)
            self.screen.blit(lines_text, (info_x, y_offset + 60))
            
            bump_color = self.RED if evaluation['bumpiness'] > 10 else self.WHITE
            bump_text = self.small_font.render(f"Bumpiness: {evaluation['bumpiness']:.1f}", True, bump_color)
            self.screen.blit(bump_text, (info_x, y_offset + 80))
    
    def draw_controls(self):
        control_x = self.BOARD_WIDTH + self.SIDEBAR_WIDTH + 20
        control_y = 330
        
        title = self.large_font.render("AI Controls", True, self.WHITE)
        self.screen.blit(title, (control_x, 10))
        
        instructions = [
            "Adjust sliders to tune AI:",
            "",
            "P - Pause",
            "ESC - Quit",
            "R - Restart (when game over)",
            "",
            "Optimal values vary based",
            "on playing style preference."
        ]
        
        for i, text in enumerate(instructions):
            rendered = self.small_font.render(text, True, self.WHITE)
            self.screen.blit(rendered, (control_x, control_y + i * 20))
    
    def draw_sliders(self):
        for slider in self.sliders:
            slider.draw(self.screen, self.small_font)
    
    def draw_game_over(self):
        if self.game.game_over:
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            game_over_text = self.large_font.render("GAME OVER", True, self.WHITE)
            score_text = self.font.render(f"Final Score: {self.game.score}", True, self.WHITE)
            lines_text = self.font.render(f"Lines Cleared: {self.game.lines_cleared}", True, self.WHITE)
            restart_text = self.font.render("Press R to restart", True, self.WHITE)
            
            game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 60))
            score_rect = score_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 - 20))
            lines_rect = lines_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 10))
            restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2 + 50))
            
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(score_text, score_rect)
            self.screen.blit(lines_text, lines_rect)
            self.screen.blit(restart_text, restart_rect)
    
    def draw_paused(self):
        if self.game.paused:
            overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
            overlay.set_alpha(128)
            overlay.fill(self.BLACK)
            self.screen.blit(overlay, (0, 0))
            
            paused_text = self.large_font.render("PAUSED", True, self.WHITE)
            text_rect = paused_text.get_rect(center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
            self.screen.blit(paused_text, text_rect)
    
    def handle_slider_events(self, event):
        for slider in self.sliders:
            slider.handle_event(event)
    
    def get_slider_values(self):
        return [slider.val for slider in self.sliders]
    
    def render(self, ai_controls):
        self.screen.fill(self.BLACK)
        
        self.draw_board()
        
        if not self.game.game_over and not self.game.paused:
            self.draw_ghost_piece()
            self.draw_piece(self.game.current_piece)
        
        self.draw_next_piece()
        self.draw_score()
        self.draw_ai_info(ai_controls)
        self.draw_controls()
        self.draw_sliders()
        self.draw_game_over()
        self.draw_paused()
        
        pygame.display.flip()

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    game = TetrisGame()
    renderer = AITetrisRenderer(game)
    ai_controls = AIControls()
    
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
                    ai_controls.handle_event(event)
            else:
                ai_controls.handle_event(event)
                renderer.handle_slider_events(event)
        
        slider_values = renderer.get_slider_values()
        ai_controls.set_ai_weights(slider_values[0], slider_values[1], slider_values[2], slider_values[3])
        
        if ai_controls.is_quit_pressed():
            running = False
        
        if not game.game_over:
            if ai_controls.is_pause_pressed():
                game.toggle_pause()
            
            if not game.paused:
                ai_controls.update_ai(game, dt)
                
                if ai_controls.is_left_pressed():
                    game.move_piece(-1, 0)
                elif ai_controls.is_right_pressed():
                    game.move_piece(1, 0)
                
                if ai_controls.is_rotate_pressed():
                    game.rotate_piece()
                
                if ai_controls.is_hard_drop_pressed():
                    game.hard_drop()
                
                game.update(dt)
        
        renderer.render(ai_controls)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()