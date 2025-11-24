import pygame
import sys
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
