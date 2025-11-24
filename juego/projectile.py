import pygame
from constants import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed, is_player):
        super().__init__()
        self.image = pygame.Surface((15, 15))
        if is_player:
            self.image.fill(AZUL_MAGICO) # Bola de fuego azul
        else:
            self.image.fill(ROJO_OSCURO) # Ataque enemigo
            
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = direction * speed
        self.is_player = is_player
        self.damage = 10

    def update(self):
        self.rect.center += self.velocity
        if not self.rect.colliderect(pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)):
            self.kill()
