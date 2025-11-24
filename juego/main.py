import pygame
import sys
# import file jugador

from jugador import Player
from constants import *
from spritemanager import SpriteManager
from riu import Riu
from pit import Pit
from melkin import Melkin


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Martin vs The Bosses")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 30)
        
        # Cargar Sprites con la nueva logica
        self.sprite_manager = SpriteManager("juego/sprites_sheet.png")
        
        self.state = "MENU"
        self.level = 0
        self.boss_classes = [Riu, Pit, Melkin]
        
    def start_game(self):
        self.player = Player(self.sprite_manager)
        self.projectiles = pygame.sprite.Group()
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        self.boss = None
        self.level = 0
        self.spawn_boss()
        self.state = "PLAYING"

    def spawn_boss(self):
        if self.level < len(self.boss_classes):
            BossClass = self.boss_classes[self.level]
            self.boss = BossClass(self.sprite_manager)
            self.all_sprites.add(self.boss)
            # Reset jugador pos
            self.player.rect.center = (ANCHO_PANTALLA//2, ALTO_PANTALLA - 100)
        else:
            self.state = "VICTORY"

    def draw_text(self, text, y_pos, color=BLANCO, size=30):
        font = pygame.font.SysFont("Arial", size, bold=True)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(ANCHO_PANTALLA//2, y_pos))
        self.screen.blit(surf, rect)

    def run(self):
        while True:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if self.state == "MENU":
                    if event.key == pygame.K_RETURN:
                        self.start_game()
                    if event.key == pygame.K_c:
                        self.state = "CREDITS"
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit(); sys.exit()
                
                elif self.state == "CREDITS":
                    if event.key == pygame.K_ESCAPE: self.state = "MENU"
                
                elif self.state == "PLAYING":
                    if event.key == pygame.K_SPACE:
                        self.player.shoot(None, self.projectiles)
                
                elif self.state in ["GAMEOVER", "VICTORY"]:
                    if event.key == pygame.K_RETURN:
                        self.state = "MENU"

    def update(self):
        if self.state == "PLAYING":
            self.player.update()
            self.projectiles.update()
            
            if self.boss:
                self.boss.update()
                self.boss.ai_update(self.player, self.projectiles)
                
                # Colisiones Proyectil -> Jefe
                hits = [p for p in self.projectiles if p.is_player and p.rect.colliderect(self.boss.hitbox)]
                for p in hits:
                    self.boss.hp -= p.damage
                    p.kill()
                
                # Colisiones Proyectil -> Jugador
                hits = [p for p in self.projectiles if not p.is_player and p.rect.colliderect(self.player.hitbox)]
                for p in hits:
                    self.player.hp -= p.damage
                    p.kill()

                # Colision Cuerpo a Cuerpo
                if self.player.hitbox.colliderect(self.boss.hitbox):
                    self.player.hp -= 1 # Daño por contacto

                # Verificar muertes
                if self.boss.hp <= 0:
                    self.boss.kill()
                    self.level += 1
                    if self.level >= len(self.boss_classes):
                        self.state = "VICTORY"
                    else:
                        self.spawn_boss() # Siguiente Boss
                
                if self.player.hp <= 0:
                    self.state = "GAMEOVER"

    def draw(self):
        self.screen.fill((20, 20, 30)) # Fondo sala
        
        if self.state == "MENU":
            self.draw_text("MARTIN VS BOSSES", 150, AZUL_MAGICO, 60)
            self.draw_text("Presiona ENTER para Empezar", 300)
            self.draw_text("Presiona C para Creditos", 350)
            
        elif self.state == "CREDITS":
            self.draw_text("CREDITOS", 100, BLANCO, 40)
            self.draw_text("Programacion: Juan David & Gemini", 250)
            self.draw_text("Arte: Gemini Gen AI", 300)
            self.draw_text("ESC para volver", 500)
            
        elif self.state == "PLAYING":
            # Dibujar suelo
            pygame.draw.rect(self.screen, (40, 40, 50), (50, 50, ANCHO_PANTALLA-100, ALTO_PANTALLA-100))
            
            self.all_sprites.draw(self.screen)
            self.projectiles.draw(self.screen)
            
            # Barras de Vida
            self.player.draw_health(self.screen)
            if self.boss and self.boss.alive():
                self.boss.draw_health(self.screen)
                self.draw_text(self.boss.name, 30, ROJO_OSCURO, 20)

        elif self.state == "GAMEOVER":
            self.draw_text("HAS MUERTO", 250, ROJO_OSCURO, 50)
            self.draw_text("Enter para Menu", 350)
            
        elif self.state == "VICTORY":
            self.draw_text("¡VICTORIA!", 250, VERDE_UI, 50)
            self.draw_text("Todos los jefes han sido derrotados", 320)
            self.draw_text("Enter para Menu", 400)

        pygame.display.flip()

if __name__ == "__main__":
    Game().run()