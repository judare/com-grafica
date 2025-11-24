import pygame
from boss import Boss
from constants import *
from projectile import Projectile

class Pit(Boss): # El Arquero
    def __init__(self, sprite_manager):
        super().__init__("Pit El Arquero", 150, sprite_manager, 2) # ID 2
        self.speed = 3
        self.strafe_dir = 1
    
    def ai_update(self, player, projectile_group):
        # Moverse de lado a lado arriba
        self.rect.x += self.speed * self.strafe_dir
        if self.rect.right > ANCHO_PANTALLA or self.rect.left < 0:
            self.strafe_dir *= -1
            self.facing_right = not self.facing_right
        
        self.state = "run"
        
        # Disparar
        self.action_timer += 1
        if self.action_timer > 100:
            self.action_timer = 0
            self.state = "attack"
            dir_to_player = (pygame.math.Vector2(player.rect.center) - pygame.math.Vector2(self.rect.center)).normalize()
            proj = Projectile(self.rect.centerx, self.rect.centery, dir_to_player, 7, False)
            projectile_group.add(proj)
