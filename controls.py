import pygame

class Controls:
    def __init__(self):
        self.actions = {
            'left': False,
            'right': False,
            'down': False,
            'rotate': False,
            'hard_drop': False,
            'pause': False,
            'quit': False
        }
        
        self.key_repeat_delay = 150
        self.key_repeat_interval = 50
        self.last_move_time = 0
        
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.actions['left'] = True
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.actions['right'] = True
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.actions['down'] = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w or event.key == pygame.K_SPACE:
                self.actions['rotate'] = True
            elif event.key == pygame.K_z:
                self.actions['hard_drop'] = True
            elif event.key == pygame.K_p:
                self.actions['pause'] = True
            elif event.key == pygame.K_ESCAPE:
                self.actions['quit'] = True
                
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.actions['left'] = False
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.actions['right'] = False
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.actions['down'] = False
                
    def get_action(self, action_name):
        return self.actions.get(action_name, False)
    
    def reset_single_actions(self):
        self.actions['rotate'] = False
        self.actions['hard_drop'] = False
        self.actions['pause'] = False
        self.actions['quit'] = False
    
    def is_left_pressed(self):
        return self.actions['left']
    
    def is_right_pressed(self):
        return self.actions['right']
    
    def is_down_pressed(self):
        return self.actions['down']
    
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