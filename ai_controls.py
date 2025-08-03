import pygame
from ai_player import TetrisAI

class AIControls:
    def __init__(self):
        self.ai = TetrisAI()
        self.current_move_sequence = []
        self.move_timer = 0
        self.move_delay = 100
        self.thinking_delay = 200
        self.last_think_time = 0
        self.current_best_move = None
        
        self.actions = {
            'left': False,
            'right': False,
            'down': False,
            'rotate': False,
            'hard_drop': False,
            'pause': False,
            'quit': False
        }
    
    def set_ai_weights(self, hole_weight, landing_height_weight, lines_cleared_weight=10.0, bumpiness_weight=-2.0):
        self.ai.set_weights(hole_weight, landing_height_weight, lines_cleared_weight, bumpiness_weight)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.actions['pause'] = True
            elif event.key == pygame.K_ESCAPE:
                self.actions['quit'] = True
        elif event.type == pygame.KEYUP:
            pass
    
    def update_ai(self, game, dt):
        if game.game_over or game.paused:
            return
        
        self.move_timer += dt
        self.last_think_time += dt
        
        if not self.current_move_sequence and self.last_think_time >= self.thinking_delay:
            self.current_best_move = self.ai.get_best_move(game)
            if self.current_best_move:
                self.current_move_sequence = self.ai.get_move_sequence(
                    game, 
                    self.current_best_move['rotation'], 
                    self.current_best_move['x']
                )
            self.last_think_time = 0
        
        if self.current_move_sequence and self.move_timer >= self.move_delay:
            next_move = self.current_move_sequence.pop(0)
            
            if next_move == 'left':
                self.actions['left'] = True
            elif next_move == 'right':
                self.actions['right'] = True
            elif next_move == 'rotate':
                self.actions['rotate'] = True
            elif next_move == 'hard_drop':
                self.actions['hard_drop'] = True
            
            self.move_timer = 0
    
    def get_action(self, action_name):
        return self.actions.get(action_name, False)
    
    def reset_single_actions(self):
        self.actions['rotate'] = False
        self.actions['hard_drop'] = False
        self.actions['pause'] = False
        self.actions['quit'] = False
        self.actions['left'] = False
        self.actions['right'] = False
    
    def is_left_pressed(self):
        action = self.actions['left']
        if action:
            self.actions['left'] = False
        return action
    
    def is_right_pressed(self):
        action = self.actions['right']
        if action:
            self.actions['right'] = False
        return action
    
    def is_down_pressed(self):
        return False
    
    def is_rotate_pressed(self):
        action = self.actions['rotate']
        if action:
            self.actions['rotate'] = False
        return action
    
    def is_hard_drop_pressed(self):
        action = self.actions['hard_drop']
        if action:
            self.actions['hard_drop'] = False
        return action
    
    def is_pause_pressed(self):
        action = self.actions['pause']
        if action:
            self.actions['pause'] = False
        return action
    
    def is_quit_pressed(self):
        return self.actions['quit']
    
    def get_current_evaluation(self):
        if self.current_best_move:
            return {
                'score': self.current_best_move['score'],
                'holes': self.current_best_move['holes'],
                'landing_height': self.current_best_move['landing_height'],
                'lines_cleared': self.current_best_move['lines_cleared'],
                'bumpiness': self.current_best_move['bumpiness']
            }
        return None