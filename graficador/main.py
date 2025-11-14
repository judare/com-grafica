# -*- coding: utf-8 -*-

import pygame
import math
# import all from functions

from functions import *

pygame.init()

# -----------------------------
# Configuración general
# -----------------------------
ANCHO, ALTO = 1000, 680
ANCHO_PANEL = 230
FPS = 60

# --- Colores UI ---
COLOR_BG = (28, 28, 32)
COLOR_PANEL = (20, 20, 24)
COLOR_TEXTO = (240, 240, 240)
COLOR_TEXTO_PANEL = (200, 200, 200)
COLOR_BORDE = (70, 70, 80)
COLOR_BOTON = (60, 62, 68)
COLOR_BOTON_HOVER = (80, 82, 90)
COLOR_BOTON_ACTIVO = (100, 110, 190) # Color para herramienta activa
COLOR_BOTON_ACCION = (80, 60, 60) # Para Limpiar/Deshacer
COLOR_BOTON_ACCION_HOVER = (100, 80, 80)

# --- Colores Canvas ---
COLOR_CANVAS = (255, 255, 255)
COLOR_GRID = (230, 230, 235)
COLOR_AXES = (120, 120, 120)
COLOR_PREVIEW = (30, 144, 255) # Azul para vista previa
COLOR_CONTROL_POINT = (255, 0, 0) # Rojo para puntos de control

# --- Paleta de Colores ---
PALETA_COLORES = [
    (0, 0, 0),       # Negro
    (255, 0, 0),     # Rojo
    (0, 255, 0),     # Verde
    (0, 0, 255),     # Azul
    (255, 255, 0),   # Amarillo
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (128, 128, 128), # Gris
]
COLOR_DIBUJO_DEFAULT = PALETA_COLORES[0]


# ---------------------------------------------------------------------
# --- ALGORITMOS GRAFICOS ---
# (Implementaciones manuales como requiere el PDF)
# ---------------------------------------------------------------------

# -----------------------------
# Clase Boton (UI)
# -----------------------------
class Boton:
    def __init__(self, x, y, w, h, texto, on_click=None,
                 color=COLOR_BOTON, color_hover=COLOR_BOTON_HOVER,
                 color_texto=COLOR_TEXTO, fuente=None, data=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.on_click = on_click
        self.color = color
        self.color_hover = color_hover
        self.color_activo = COLOR_BOTON_ACTIVO
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 24)
        self.hover = False
        self.activo = False # Para botones de selección de herramienta
        self.visible = True
        self.data = data # Para guardar datos (ej. el color de un botón)

    def draw(self, surface):
        if not self.visible:
            return
            
        col = self.color
        if self.activo:
            col = self.color_activo
        elif self.hover:
            col = self.color_hover
            
        pygame.draw.rect(surface, col, self.rect, border_radius=8)
        pygame.draw.rect(surface, COLOR_BORDE, self.rect, width=1, border_radius=8)
        
        if self.texto:
            text_surf = self.fuente.render(self.texto, True, self.color_texto)
            text_rect = text_surf.get_rect(center=self.rect.center)
            surface.blit(text_surf, text_rect)

    def handle(self, events):
        if not self.visible:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
                if self.on_click:
                    # Si el botón tiene 'data', la pasa al callback
                    if self.data is not None:
                        self.on_click(self.data)
                    else:
                        self.on_click()
                return True
        return False

# -----------------------------
# Utilidades de dibujo
# -----------------------------
def draw_grid_and_axes(surface, show_grid, show_axes):
    surface.fill(COLOR_CANVAS)
    if show_grid:
        w, h = surface.get_size()
        for x in range(0, w, 20):
            pygame.draw.line(surface, COLOR_GRID, (x, 0), (x, h))
        for y in range(0, h, 20):
            pygame.draw.line(surface, COLOR_GRID, (0, y), (w, y))
    
    if show_axes:
        w, h = surface.get_size()
        cx, cy = w // 2, h // 2
        pygame.draw.line(surface, COLOR_AXES, (0, cy), (w, cy), 1) # eje X
        pygame.draw.line(surface, COLOR_AXES, (cx, 0), (cx, h), 1) # eje Y

def rect_from_points(p0, p1):
    (x0, y0), (x1, y1) = p0, p1
    x = min(x0, x1)
    y = min(y0, y1)
    w = abs(x1 - x0)
    h = abs(y1 - y0)
    return pygame.Rect(x, y, w, h)

# -----------------------------
# App Graficador
# -----------------------------
class GraficadorApp:
    def __init__(self):
        self.screen = pygame.display.set_mode((ANCHO, ALTO))
        pygame.display.set_caption("Graficador Manual - Pygame (Cumple PDF)")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 28)
        self.font_text = pygame.font.Font(None, 24)
        self.font_status = pygame.font.Font(None, 22)

        # Superficie de dibujo (canvas)
        self.canvas = pygame.Surface((ANCHO - ANCHO_PANEL - 20, ALTO - 40))
        self.canvas_rect = self.canvas.get_rect(topleft=(ANCHO_PANEL + 10, 20))

        # Estado
        self.herramienta = "Linea (Bresenham)"
        self.color_actual = COLOR_DIBUJO_DEFAULT
        self.mostrando_grid = True
        self.mostrando_ejes = True
        
        # Estado para herramientas de 2 puntos (arrastrar)
        self.dibujando = False
        self.p_ini = None
        self.p_fin = None
        
        # Estado para herramientas de N puntos (clics)
        self.control_points = []
        self.mouse_pos_canvas = (0, 0) # Posición actual del mouse en el canvas
        
        # Almacen de figuras
        self.figuras = []  # lista de dicts: {"tipo":..., "puntos":[p0, p1...], "color":...}

        self.botones = {} # Diccionario de botones
        self.tool_buttons = [] # Lista de botones de herramienta (para activar/desactivar)
        self.color_buttons = [] # Lista de botones de color
        self._crear_botones()
        
        self.limpiar_canvas(redibujar=False)
        self.actualizar_botones_herramienta()

    def _crear_botones(self):
        x, y = 15, 20
        w, h = ANCHO_PANEL - 30, 38
        sep = 8

        # --- Título Herramientas ---
        self.screen.blit(self.font_title.render("Herramientas", True, COLOR_TEXTO), (x, y))
        y += 40

        # --- Botones de Herramientas ---
        tools = [
            "Linea (DDA)", "Linea (Bresenham)", "Rectangulo", 
            "Circulo (Bresenham)", "Elipse", "Triangulo",
            "Curva Bézier", "Poligono"
        ]
        
        for i, tool_name in enumerate(tools):
            b = Boton(x, y + i*(h+sep), w, h, tool_name, on_click=self.set_tool(tool_name))
            self.botones[tool_name] = b
            self.tool_buttons.append(b)
        
        y_sep1 = y + len(tools)*(h+sep) + 10

        # --- Botones de Acciones ---
        b_deshacer = Boton(x, y_sep1, w, h, "Deshacer", on_click=self.deshacer, 
                           color=COLOR_BOTON_ACCION, color_hover=COLOR_BOTON_ACCION_HOVER)
        b_limpiar = Boton(x, y_sep1 + (h+sep), w, h, "Limpiar", on_click=self.vaciar_figuras,
                          color=COLOR_BOTON_ACCION, color_hover=COLOR_BOTON_ACCION_HOVER)
        self.botones["Deshacer"] = b_deshacer
        self.botones["Limpiar"] = b_limpiar

        y_sep2 = y_sep1 + 2*(h+sep) + 10

        # --- Botones de Opciones ---
        b_grid = Boton(x, y_sep2, w, h, "Toggle Cuadrícula", on_click=self.toggle_grid)
        b_axes = Boton(x, y_sep2 + (h+sep), w, h, "Toggle Ejes", on_click=self.toggle_axes)
        b_grid.activo = self.mostrando_grid
        b_axes.activo = self.mostrando_ejes
        self.botones["Grid"] = b_grid
        self.botones["Ejes"] = b_axes

        y_sep3 = y_sep2 + 2*(h+sep) + 10
        
        # --- Botón Finalizar Polígono (inicialmente oculto) ---
        b_finish = Boton(x, y_sep3, w, h, "Finalizar Poligono", on_click=self.finalizar_poligono,
                         color=(60, 80, 60), color_hover=(80, 100, 80))
        b_finish.visible = False
        self.botones["Finalizar"] = b_finish

        # --- Paleta de Colores ---
        self.screen.blit(self.font_text.render("Colores", True, COLOR_TEXTO), (x, y_sep3 + 30))
        y_col = y_sep3 + 60
        cw, ch = 24, 24 # Tamaño botón de color
        csep = 6
        cols_per_row = 6
        for i, color in enumerate(PALETA_COLORES):
            row = i // cols_per_row
            col = i % cols_per_row
            cx = x + col * (cw + csep)
            cy = y_col + row * (ch + csep)
            
            b_col = Boton(cx, cy, cw, ch, "", on_click=self.set_color, 
                          color=color, color_hover=color, data=color)
            self.botones[f"color_{i}"] = b_col
            self.color_buttons.append(b_col)
        
        # Marcar primer color como activo
        self.color_buttons[0].activo = True

    # ----------------- Callbacks Botones -----------------
    
    def set_tool(self, nombre_herramienta):
        def _callback():
            # Si cambiamos de herramienta, limpiamos los puntos de control
            if self.herramienta != nombre_herramienta:
                self.control_points.clear()
                self.dibujando = False
                
            self.herramienta = nombre_herramienta
            self.actualizar_botones_herramienta()
        return _callback

    def actualizar_botones_herramienta(self):
        # Desactivar todos los botones de herramienta
        for b in self.tool_buttons:
            b.activo = (b.texto == self.herramienta)
        
        # Mostrar/ocultar "Finalizar Poligono"
        es_poligono = self.herramienta == "Poligono"
        tiene_puntos = len(self.control_points) > 1 # Necesita al menos 2 puntos
        self.botones["Finalizar"].visible = es_poligono and tiene_puntos

    def set_color(self, color):
        self.color_actual = color
        for b in self.color_buttons:
            b.activo = (b.data == color)

    def deshacer(self):
        if self.figuras:
            self.figuras.pop()
            self.limpiar_canvas()

    def vaciar_figuras(self):
        self.figuras.clear()
        self.limpiar_canvas()

    def toggle_grid(self):
        self.mostrando_grid = not self.mostrando_grid
        self.botones["Grid"].activo = self.mostrando_grid
        self.limpiar_canvas()

    def toggle_axes(self):
        self.mostrando_ejes = not self.mostrando_ejes
        self.botones["Ejes"].activo = self.mostrando_ejes
        self.limpiar_canvas()

    def finalizar_poligono(self):
        if self.herramienta == "Poligono" and len(self.control_points) > 1:
            # Cierra el polígono conectando el último punto con el primero
            self.control_points.append(self.control_points[0]) 
            self.registrar_figura_multipunto()

    def limpiar_canvas(self, redibujar=True):
        draw_grid_and_axes(self.canvas, self.mostrando_grid, self.mostrando_ejes)
        if redibujar:
            for f in self.figuras:
                self._dibujar_figura_persistente(self.canvas, f)

    # ----------------- Lógica de Estado (Herramientas) -----------------
    
    def is_multi_point_tool(self):
        return self.herramienta in ["Triangulo", "Curva Bézier", "Poligono"]

    def get_required_points(self):
        if self.herramienta == "Triangulo": return 3
        if self.herramienta == "Curva Bézier": return 4
        if self.herramienta == "Poligono": return 1000 # "Infinito" hasta finalizar
        return 2 # Para herramientas de 2 puntos

    def get_status_message(self):
        if self.is_multi_point_tool():
            req = self.get_required_points()
            curr = len(self.control_points)
            if self.herramienta == "Poligono":
                if curr == 0:
                    return "Click para primer punto de Polígono"
                elif curr == 1:
                    return "Click para sgte. punto (o Finalizar)"
                else:
                    return f"Puntos: {curr}. Click para sgte. (o Finalizar)"
            else:
                return f"Click para punto {curr + 1} de {req} ({self.herramienta})"
        else:
            return f"Herramienta: {self.herramienta}. Arrastre para dibujar."

    # ----------------- Lógica de Eventos -----------------

    def manejador_eventos(self):
        eventos = pygame.event.get()
        
        # Actualizar posición del mouse relativa al canvas
        mx, my = pygame.mouse.get_pos()
        self.mouse_pos_canvas = (
            max(0, min(self.canvas_rect.w - 1, mx - self.canvas_rect.x)),
            max(0, min(self.canvas_rect.h - 1, my - self.canvas_rect.y))
        )
            
        for e in eventos:
            if e.type == pygame.QUIT:
                return False

            # --- Clics del Mouse ---
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Ignorar clics fuera del canvas
                if self.canvas_rect.collidepoint(e.pos):
                    if self.is_multi_point_tool():
                        self.handle_multipoint_click(self.mouse_pos_canvas)
                    else:
                        # Iniciar dibujo de 2 puntos
                        self.dibujando = True
                        self.p_ini = self.mouse_pos_canvas
                        self.p_fin = self.mouse_pos_canvas
            
            # --- Movimiento del Mouse ---
            elif e.type == pygame.MOUSEMOTION:
                if self.dibujando and not self.is_multi_point_tool():
                    self.p_fin = self.mouse_pos_canvas

            # --- Soltar Clic ---
            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if self.dibujando and not self.is_multi_point_tool():
                    # Finalizar dibujo de 2 puntos
                    self.dibujando = False
                    self.registrar_figura_2puntos()
                    self.p_ini, self.p_fin = None, None

        # Manejo de botones (después de eventos de canvas)
        for b in self.botones.values():
            b.handle(eventos)

        return True

    def handle_multipoint_click(self, canvas_pos):
        self.control_points.append(canvas_pos)
        req_points = self.get_required_points()
        
        if len(self.control_points) == req_points:
            self.registrar_figura_multipunto()
        
        self.actualizar_botones_herramienta()

    def registrar_figura_2puntos(self):
        # Solo registrar si los puntos son distintos
        if self.p_ini == self.p_fin:
            return
            
        figura = {
            "tipo": self.herramienta, 
            "puntos": [self.p_ini, self.p_fin],
            "color": self.color_actual
        }
        self.figuras.append(figura)
        # Dibuja la figura final en el canvas persistente
        self._dibujar_figura_persistente(self.canvas, figura)

    def registrar_figura_multipunto(self):
        figura = {
            "tipo": self.herramienta,
            "puntos": list(self.control_points), # Copiar la lista
            "color": self.color_actual
        }
        self.figuras.append(figura)
        self._dibujar_figura_persistente(self.canvas, figura)
        
        # Limpiar para la siguiente figura
        self.control_points.clear()
        self.actualizar_botones_herramienta()

    # ----------------- Lógica de Dibujo (Rendering) -----------------
    
    def _dibujar_figura_persistente(self, surface, fig):
        """
        Dibuja una figura en el canvas persistente.
        Usa los algoritmos manuales.
        """
        tipo = fig["tipo"]
        puntos = fig["puntos"]
        color = fig["color"]
        p0 = puntos[0]
        
        # --- Figuras de 2 Puntos ---
        if tipo in ["Linea (DDA)", "Linea (Bresenham)", "Rectangulo", "Circulo (Bresenham)", "Elipse"]:
            if len(puntos) < 2: return
            p1 = puntos[1]

            if tipo == "Linea (DDA)":
                dda(surface, color, p0, p1)
            
            elif tipo == "Linea (Bresenham)":
                bresenham_line(surface, color, p0, p1)

            elif tipo == "Rectangulo":
                rect = rect_from_points(p0, p1)
                bresenham_line(surface, color, rect.topleft, rect.topright)
                bresenham_line(surface, color, rect.topright, rect.bottomright)
                bresenham_line(surface, color, rect.bottomright, rect.bottomleft)
                bresenham_line(surface, color, rect.bottomleft, rect.topleft)

            elif tipo == "Circulo (Bresenham)":
                dx, dy = p1[0] - p0[0], p1[1] - p0[1]
                r = int(math.hypot(dx, dy))
                bresenham_circle(surface, color, p0, r)

            elif tipo == "Elipse":
                rx = abs(p1[0] - p0[0])
                ry = abs(p1[1] - p0[1])
                midpoint_ellipse(surface, color, p0, rx, ry)

        # --- Figuras Multi-Punto ---
        elif tipo == "Triangulo":
            if len(puntos) < 3: return
            bresenham_line(surface, color, puntos[0], puntos[1])
            bresenham_line(surface, color, puntos[1], puntos[2])
            bresenham_line(surface, color, puntos[2], puntos[0])

        elif tipo == "Curva Bézier":
            if len(puntos) < 4: return
            bezier_curve(surface, color, puntos[0], puntos[1], puntos[2], puntos[3])

        elif tipo == "Poligono":
            if len(puntos) < 2: return
            for i in range(len(puntos) - 1):
                bresenham_line(surface, color, puntos[i], puntos[i+1])
            # La conexión final ya está en la lista de puntos (ver finalizar_poligono)

    def _dibujar_preview(self, surface):
        """
        Dibuja la vista previa "rubber band" en una superficie temporal.
        """
        # --- Preview para herramientas de 2 puntos (arrastrar) ---
        if self.dibujando and self.p_ini and self.p_fin and not self.is_multi_point_tool():
            # Simula una figura con los puntos actuales
            preview_fig = {
                "tipo": self.herramienta,
                "puntos": [self.p_ini, self.p_fin],
                "color": COLOR_PREVIEW
            }
            self._dibujar_figura_persistente(surface, preview_fig)

        # --- Preview para herramientas multi-punto (clics) ---
        elif self.is_multi_point_tool() and self.control_points:
            # Dibuja puntos de control
            for p in self.control_points:
                pygame.draw.circle(surface, COLOR_CONTROL_POINT, p, 4) # Círculo relleno
                pygame.draw.circle(surface, COLOR_DIBUJO_DEFAULT, p, 4, 1) # Borde

            # Dibuja líneas entre puntos de control
            last_p = self.control_points[0]
            for p in self.control_points[1:]:
                dda(surface, COLOR_PREVIEW, last_p, p) # DDA para preview
                last_p = p
            
            # Dibuja línea "rubber band" hasta el mouse
            dda(surface, COLOR_PREVIEW, last_p, self.mouse_pos_canvas)
            
            # Preview específico para Bézier
            if self.herramienta == "Curva Bézier" and len(self.control_points) == 3:
                # Muestra la curva final mientras se mueve el 4to punto
                preview_fig = {
                    "tipo": "Curva Bézier",
                    "puntos": self.control_points + [self.mouse_pos_canvas],
                    "color": COLOR_PREVIEW
                }
                self._dibujar_figura_persistente(surface, preview_fig)

    # ----------------- Bucle Principal -----------------
    def run(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejador_eventos()

            # --- Dibujar Fondo y Panel ---
            self.screen.fill(COLOR_BG)
            panel_rect = pygame.Rect(0, 0, ANCHO_PANEL, ALTO)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)
            pygame.draw.line(self.screen, COLOR_BORDE, (ANCHO_PANEL, 0), (ANCHO_PANEL, ALTO), 1)

            # --- Dibujar Botones ---
            for b in self.botones.values():
                b.draw(self.screen)

            # --- Dibujar Canvas ---
            # 1. Mostramos la versión persistente (el canvas real)
            self.screen.blit(self.canvas, self.canvas_rect)

            # 2. Dibujamos la vista previa (temporal) por encima
            if self.dibujando or (self.is_multi_point_tool() and self.control_points):
                # Dibujamos preview en una copia para no alterar el canvas real
                preview_surface = self.canvas.copy()
                self._dibujar_preview(preview_surface)
                self.screen.blit(preview_surface, self.canvas_rect)

            # 3. Dibujar borde del canvas
            pygame.draw.rect(self.screen, COLOR_BORDE, self.canvas_rect, 1)

            # --- Etiquetas de estado ---
            msg = self.get_status_message()
            txt_status = self.font_status.render(msg, True, COLOR_TEXTO_PANEL)
            self.screen.blit(txt_status, (ANCHO_PANEL + 14, ALTO - 24))

            pygame.display.flip()
            self.clock.tick(FPS)

# -----------------------------
# Ejecutar
# -----------------------------
if __name__ == "__main__":
    app = GraficadorApp()
    app.run()
