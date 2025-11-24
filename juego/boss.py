import pygame
from entity import Entity
from constants import *
# --- CLASES DEL JUEGO (POO) ---

class Boss(Entity):
    def __init__(self, name, hp, sprite_manager, char_idx):
        super().__init__(ANCHO_PANTALLA // 2, 150, hp)
        self.name = name
        
        # Cargar Animaciones según el ID del personaje en la hoja
        self.animations['idle'] = sprite_manager.get_animation(char_idx, 0, 4)
        self.animations['run'] = sprite_manager.get_animation(char_idx, 1, 4)
        self.animations['attack'] = sprite_manager.get_animation(char_idx, 2, 4)
        
        self.image = self.animations['idle'][0]
        self.action_timer = 0
        self.target = None

    def ai_update(self, player, projectile_group):
        # IA genérica, se sobrescribe en hijos
        pass

    def update(self):
        self.animate()
