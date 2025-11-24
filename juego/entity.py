import pygame
from constants import *

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, hp):
        super().__init__()
        self.hp = hp
        self.hp_max = hp
        self.animations = {} # Diccionario de listas de superficies
        self.state = "idle"
        self.frame_index = 0
        self.anim_speed = 0.15
        self.image = pygame.Surface((64, 64))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.facing_right = True

    def animate(self):
        animation = self.animations.get(self.state, self.animations.get('idle'))
        if not animation: return

        self.frame_index += self.anim_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
            
        # Obtener frame actual
        raw_image = animation[int(self.frame_index)]
        
        # Voltear si mira a la izquierda
        if not self.facing_right:
            self.image = pygame.transform.flip(raw_image, True, False)
        else:
            self.image = raw_image
            
        # Actualizar rect pero mantener centro (importante para evitar temblores)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
        # Hitbox más pequeña para colisiones justas
        self.hitbox = self.rect.inflate(-40, -40)

    def draw_health(self, surface):
        if self.hp < 0: self.hp = 0
        ratio = self.hp / self.hp_max
        bar_w = 60
        bar_h = 8
        pos = (self.rect.centerx - bar_w // 2, self.rect.top - 15)
        
        pygame.draw.rect(surface, NEGRO, (pos[0]-1, pos[1]-1, bar_w+2, bar_h+2))
        pygame.draw.rect(surface, ROJO_OSCURO, (pos[0], pos[1], bar_w, bar_h))
        pygame.draw.rect(surface, VERDE_UI, (pos[0], pos[1], bar_w * ratio, bar_h))

