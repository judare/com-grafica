import pygame
from entity import Entity
from projectile import Projectile
from constants import *

class Player(Entity):
    def __init__(self, sprite_manager):
        super().__init__(ANCHO_PANTALLA // 2, ALTO_PANTALLA - 150, 100)
        self.speed = 5
        
        # Cargar animaciones Martin (ID 0)
        # Row 0: Idle, Row 1: Jump/Run, Row 2: Attack
        self.animations['idle'] = sprite_manager.get_animation(0, 0, 4)
        self.animations['run'] = sprite_manager.get_animation(0, 1, 4)
        self.animations['attack'] = sprite_manager.get_animation(0, 2, 4)
        
        self.image = self.animations['idle'][0]
        self.last_shot = 0
        self.cooldown = 400

    def input(self):
        keys = pygame.key.get_pressed()
        self.velocity = pygame.math.Vector2(0, 0)
        
        if keys[pygame.K_UP]: self.velocity.y = -1
        if keys[pygame.K_DOWN]: self.velocity.y = 1
        if keys[pygame.K_LEFT]: self.velocity.x = -1
        if keys[pygame.K_RIGHT]: self.velocity.x = 1
        
        if self.velocity.length() > 0:
            self.velocity = self.velocity.normalize() * self.speed
            self.state = "run"
            if self.velocity.x > 0: self.facing_right = True
            elif self.velocity.x < 0: self.facing_right = False
        else:
            self.state = "idle"

    def update(self):
        self.input()
        self.rect.center += self.velocity
        
        # Limites
        self.rect.clamp_ip(pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA))
        self.animate()

    def shoot(self, target_group, projectile_group):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.cooldown:
            self.last_shot = now
            self.state = "attack" # Forzar animación visual
            # Bola de fuego
            direction = pygame.math.Vector2(1 if self.facing_right else -1, 0)
            proj = Projectile(self.rect.centerx, self.rect.centery, direction, 10, True)
            projectile_group.add(proj)
