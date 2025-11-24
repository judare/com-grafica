
import pygame
from boss import Boss
from constants import *

class Melkin(Boss): # El Jefe Final
    def __init__(self, sprite_manager):
        super().__init__("Melkin Espada", 300, sprite_manager, 3) # ID 3
        self.speed = 8 # Muy rápido (Dash)
        self.dash_cd = 0
        self.is_dashing = False
        self.dash_target = pygame.math.Vector2(0,0)

    def ai_update(self, player, projectile_group):
        if self.is_dashing:
            # Movimiento Dash
            dist = self.dash_target - pygame.math.Vector2(self.rect.center)
            if dist.length() < 10:
                self.is_dashing = False
                self.state = "idle"
            else:
                self.velocity = dist.normalize() * 15 # Super velocidad
                self.rect.center += self.velocity
                self.state = "run"
        else:
            # Preparar Dash
            self.dash_cd += 1
            self.state = "idle"
            if self.dash_cd > 60: # Cada segundo decide
                self.dash_cd = 0
                self.is_dashing = True
                self.dash_target = pygame.math.Vector2(player.rect.center)
                self.state = "attack"
                # Orientación
                if self.dash_target.x > self.rect.centerx: self.facing_right = True
                else: self.facing_right = False
