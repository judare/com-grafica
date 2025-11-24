import pygame
from boss import Boss
class Riu(Boss): # El Bruto
    def __init__(self, sprite_manager):
        super().__init__("Riu El Bruto", 200, sprite_manager, 1) # ID 1
        self.speed = 2
    
    def ai_update(self, player, projectile_group):
        # Perseguir lentamente
        dir_vec = pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)
        if dir_vec.length() > 0:
            self.velocity = dir_vec.normalize() * self.speed
        
        self.rect.center += self.velocity
        
        # Orientación
        if self.velocity.x > 0: self.facing_right = True
        else: self.facing_right = False
        
        self.state = "run" if dir_vec.length() > 50 else "attack"
