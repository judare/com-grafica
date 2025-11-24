import pygame
import sys

# --- CONSTANTES ---
ANCHO_PANTALLA = 800
ALTO_PANTALLA = 600
FPS = 60

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO_OSCURO = (150, 0, 0)
VERDE_UI = (50, 200, 50)
AZUL_MAGICO = (100, 100, 255)

# --- CLASE PARA GESTIONAR LA HOJA DE SPRITES (SOLUCIÓN AL PROBLEMA DE TAMAÑO) ---
class SpriteManager:
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
            self.sheet_w = self.sheet.get_width()
            self.sheet_h = self.sheet.get_height()
            # Asumimos que el fondo es del color del pixel (0,0) (generalmente gris en estas gens)
            self.bg_color = self.sheet.get_at((0, 0))
            self.sheet.set_colorkey(self.bg_color)
            print(f"SpriteSheet cargado: {self.sheet_w}x{self.sheet_h}")
        except pygame.error as e:
            print(f"Error cargando imagen: {e}")
            sys.exit()

    def get_animation(self, character_idx, action_row, num_frames, scale_factor=0.35):
        """
        character_idx: 0=Martin (TL), 1=Riu (TR), 2=Pit (BL), 3=Melkin (BR)
        action_row: 0=Idle (Fila 1), 1=Move (Fila 2), 2=Attack (Fila 3)
        """
        frames = []
        
        # 1. Definir el Cuadrante (La imagen se divide en 4 grandes bloques)
        quad_w = self.sheet_w // 2
        quad_h = self.sheet_h // 2
        
        col_q = character_idx % 2  # 0 o 1
        row_q = character_idx // 2 # 0 o 1
        
        base_x = col_q * quad_w
        base_y = row_q * quad_h
        
        # 2. Definir la fila dentro del cuadrante
        # Ignoramos el encabezado de texto, empezamos un poco más abajo
        header_offset = 90
        usable_height = quad_h - header_offset
        row_height = usable_height // 3
        
        current_y = base_y + header_offset + (action_row * row_height)
        
        # 3. Recortar frames
        # Asumimos aprox 4 a 5 columnas por cuadrante
        frame_width = quad_w // 7
        
        for i in range(num_frames):
            # Ajuste fino para centrar el recorte
            x = base_x + (i * frame_width)
            y = current_y
            
            # Crear subsuperficie
            rect = pygame.Rect(x, y, frame_width, row_height)
            
            try:
                image = self.sheet.subsurface(rect)
                
                # Escalar la imagen (son muy grandes originalmente)
                new_w = int(frame_width * scale_factor)
                new_h = int(row_height * scale_factor)
                image = pygame.transform.scale(image, (new_w, new_h))
                
                frames.append(image)
            except ValueError:
                pass # Si el rect se sale, ignoramos

        return frames

# --- CLASES DEL JUEGO (POO) ---

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

# --- JEFES ESPECÍFICOS ---

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

# --- CLASE PRINCIPAL ---

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
        pygame.display.set_caption("Martin vs The Bosses - 2816x1536 Fix")
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
            self.draw_text("Programacion: Gemini", 250)
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