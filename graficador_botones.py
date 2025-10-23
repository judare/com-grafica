# -*- coding: utf-8 -*-
"""
Graficador sencillo con Pygame + POO
------------------------------------
- Integra el código base del usuario (línea/rectángulo/círculo) con una barra lateral de botones.
- Permite elegir herramienta: Línea, Rectángulo, Círculo.
- Incluye: Deshacer, Limpiar, mostrar Ocultar Ejes y Cuadrícula.
- Vista previa ("rubber band") mientras arrastras el mouse.
- Dibujo persistente sobre un lienzo independiente del UI.

Requisitos:
    pip install pygame
"""

import pygame
import math

pygame.init()


# --- Definición del algoritmo DDA (de la imagen 2) ---
def dda(screen, color, pos1, pos2, width):
    x1 = pos1[0]
    y1 = pos1[1]
    x2 = pos2[0]
    y2 = pos2[1]
    """
    Objetivo: Implementar el algoritmo DDA para dibujar una línea entre dos
    puntos (x1, y1) y (x2, y2) con el color especificado.
    """
    dx = x2 - x1
    dy = y2 - y1

    # Determinar el número de pasos
    if abs(dx) > abs(dy):
        steps = int(abs(dx))
    else:
        steps = int(abs(dy))

    # Evitar división por cero si steps es 0 (puntos coincidentes)
    if steps == 0:
        pygame.draw.circle(screen, color, (round(x1), round(y1)), 1)
        return

    # Calcular incrementos
    x_inc = dx / steps
    y_inc = dy / steps

    # Inicializar coordenadas
    x, y = x1, y1

    # Dibujar los puntos (usamos steps + 1 para incluir el punto final)
    for _ in range(steps + 1):
        pygame.draw.circle(screen, color, (round(x), round(y)), 1)
        x += x_inc
        y += y_inc


# -----------------------------
# Configuración general
# -----------------------------
ANCHO, ALTO = 1000, 680
ANCHO_PANEL = 230
FPS = 60

COLOR_BG = (28, 28, 32)
COLOR_PANEL = (20, 20, 24)
COLOR_TEXTO = (240, 240, 240)
COLOR_BORDE = (70, 70, 80)

COLOR_CANVAS = (255, 255, 255)
COLOR_GRID = (230, 230, 235)
COLOR_AXES = (120, 120, 120)
COLOR_DIBUJO = (0, 0, 0)

# -----------------------------
# Clase Boton (POO)
# -----------------------------
class Boton:
    def __init__(self, x, y, w, h, texto, on_click=None,
                 color=(60, 62, 68), color_hover=(80, 82, 90),
                 color_texto=(240, 240, 240), fuente=None):
        self.rect = pygame.Rect(x, y, w, h)
        self.texto = texto
        self.on_click = on_click
        self.color = color
        self.color_hover = color_hover
        self.color_texto = color_texto
        self.fuente = fuente or pygame.font.Font(None, 28)
        self.hover = False
        self.activo = False  # Para botones de selección de herramienta

    def draw(self, surface):
        col = self.color_hover if (self.hover or self.activo) else self.color
        pygame.draw.rect(surface, col, self.rect, border_radius=10)
        pygame.draw.rect(surface, COLOR_BORDE, self.rect, width=1, border_radius=10)
        text_surf = self.fuente.render(self.texto, True, self.color_texto)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle(self, events):
        mouse_pos = pygame.mouse.get_pos()
        self.hover = self.rect.collidepoint(mouse_pos)
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 and self.hover:
                if self.on_click:
                    self.on_click()
                return True
        return False

# -----------------------------
# Utilidades de dibujo
# -----------------------------
def draw_grid(surface, spacing=20, color=COLOR_GRID):
    w, h = surface.get_size()
    for x in range(0, w, spacing):
        dda(surface, color, (x, 0), (x, h), 1)
    for y in range(0, h, spacing):
        dda(surface, color, (0, y), (w, y), 1)

def draw_axes(surface, color=COLOR_AXES, width=1):
    w, h = surface.get_size()
    cx, cy = w // 2, h // 2
    dda(surface, color, (0, cy), (w, cy), width)  # eje X
    dda(surface, color, (cx, 0), (cx, h), width)  # eje Y

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
        pygame.display.set_caption("Graficador sencillo - Pygame + POO")
        self.clock = pygame.time.Clock()
        self.font_title = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)

        # Superficie de dibujo (canvas) donde quedan persistentes las figuras
        self.canvas = pygame.Surface((ANCHO - ANCHO_PANEL - 20, ALTO - 40))
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.topleft = (ANCHO_PANEL + 10, 20)

        # Estado
        self.herramienta = "Linea"   # "Linea", "Rectangulo", "Circulo"
        self.mostrando_grid = True
        self.mostrando_ejes = True
        self.dibujando = False
        self.p_ini = None
        self.p_fin = None
        self.figuras = []  # lista de dicts: {"tipo":..., "p0":(x,y), "p1":(x,y), "color":..., "width":...}

        # Inicializar canvas
        self.limpiar_canvas()

        # Botones
        self.botones = []
        self._crear_botones()

    def limpiar_canvas(self):
        self.canvas.fill(COLOR_CANVAS)
        if self.mostrando_grid:
            draw_grid(self.canvas, spacing=20)
        if self.mostrando_ejes:
            draw_axes(self.canvas)

        # Redibujar todas las figuras existentes
        for f in self.figuras:
            self._dibujar_figura(self.canvas, f)

    def _crear_botones(self):
        x, y = 15, 20
        w, h = ANCHO_PANEL - 30, 44
        sep = 10

        def set_tool(nombre):
            def _cb():
                self.herramienta = nombre
                # Marcar activo
                for b in self.botones:
                    if b.texto in ("Linea", "Rectangulo", "Circulo"):
                        b.activo = (b.texto == nombre)
            return _cb

        b_linea = Boton(x, y, w, h, "Linea", on_click=set_tool("Linea"))
        b_linea.activo = True
        b_rect = Boton(x, y + (h+sep), w, h, "Rectangulo", on_click=set_tool("Rectangulo"))
        b_circ = Boton(x, y + 2*(h+sep), w, h, "Circulo", on_click=set_tool("Circulo"))

        y2 = y + 3*(h+sep) + 10
        b_deshacer = Boton(x, y2, w, h, "Deshacer", on_click=self.deshacer)
        b_limpiar = Boton(x, y2 + (h+sep), w, h, "Limpiar", on_click=self.vaciar_figuras)

        y3 = y2 + 2*(h+sep) + 10
        b_grid = Boton(x, y3, w, h, "Toggle Cuadrícula", on_click=self.toggle_grid)
        b_axes = Boton(x, y3 + (h+sep), w, h, "Toggle Ejes", on_click=self.toggle_axes)

        self.botones.extend([b_linea, b_rect, b_circ, b_deshacer, b_limpiar, b_grid, b_axes])

    # ----------------- acciones botones -----------------
    def deshacer(self):
        if self.figuras:
            self.figuras.pop()
            self.limpiar_canvas()

    def vaciar_figuras(self):
        self.figuras.clear()
        self.limpiar_canvas()

    def toggle_grid(self):
        self.mostrando_grid = not self.mostrando_grid
        self.limpiar_canvas()

    def toggle_axes(self):
        self.mostrando_ejes = not self.mostrando_ejes
        self.limpiar_canvas()

    # ----------------- lógica dibujo -----------------
    def manejador_eventos(self):
        eventos = pygame.event.get()
        for e in eventos:
            if e.type == pygame.QUIT:
                return False

            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                # Ignorar clicks dentro del panel
                if self.canvas_rect.collidepoint(e.pos):
                    self.dibujando = True
                    self.p_ini = (e.pos[0] - self.canvas_rect.x, e.pos[1] - self.canvas_rect.y)
                    self.p_fin = self.p_ini

            elif e.type == pygame.MOUSEMOTION and self.dibujando:
                mx, my = e.pos
                mx -= self.canvas_rect.x
                my -= self.canvas_rect.y
                # Limitar dentro del canvas
                mx = max(0, min(self.canvas.get_width()-1, mx))
                my = max(0, min(self.canvas.get_height()-1, my))
                self.p_fin = (mx, my)

            elif e.type == pygame.MOUSEBUTTONUP and e.button == 1 and self.dibujando:
                self.dibujando = False
                # Registrar figura final
                figura = {"tipo": self.herramienta, "p0": self.p_ini, "p1": self.p_fin,
                          "color": COLOR_DIBUJO, "width": 2}
                self.figuras.append(figura)
                # Dibuja definitiva en el canvas
                self._dibujar_figura(self.canvas, figura)
                self.p_ini, self.p_fin = None, None

        # Manejo de botones (después, para priorizar click en lienzo si corresponde)
        for b in self.botones:
            b.handle(eventos)

        return True

    def _dibujar_figura(self, surface, f):
        p0, p1 = f["p0"], f["p1"]
        if f["tipo"] == "Linea":
            dda(surface, f["color"], p0, p1, f["width"])
        elif f["tipo"] == "Rectangulo":
            rect = rect_from_points(p0, p1)
            pygame.draw.rect(surface, f["color"], rect, width=f["width"])
        elif f["tipo"] == "Circulo":
            dx = p1[0] - p0[0]
            dy = p1[1] - p0[1]
            r = int(math.hypot(dx, dy))
            if r > 0:
                pygame.draw.circle(surface, f["color"], p0, r, f["width"])

    def _dibujar_preview(self, surface):
        if not (self.dibujando and self.p_ini and self.p_fin):
            return
        preview = {"tipo": self.herramienta, "p0": self.p_ini, "p1": self.p_fin,
                   "color": (30, 144, 255), "width": 1}
        self._dibujar_figura(surface, preview)

    # ----------------- bucle principal -----------------
    def run(self):
        corriendo = True
        while corriendo:
            corriendo = self.manejador_eventos()

            # Fondo y panel
            self.screen.fill(COLOR_BG)
            panel_rect = pygame.Rect(0, 0, ANCHO_PANEL, ALTO)
            pygame.draw.rect(self.screen, COLOR_PANEL, panel_rect)

            # Título panel
            titulo = self.font_title.render("Herramientas", True, COLOR_TEXTO)
            self.screen.blit(titulo, (15, 0))

            # Botones
            for b in self.botones:
                b.draw(self.screen)

            # Canvas
            # Mostramos la versión persistente
            self.screen.blit(self.canvas, self.canvas_rect)

            # Vista previa por encima (temporal)
            if self.dibujando:
                # Dibujamos preview en una copia para no alterar el canvas real
                preview_surface = self.canvas.copy()
                self._dibujar_preview(preview_surface)
                self.screen.blit(preview_surface, self.canvas_rect)

            # Etiquetas de estado
            txt_tool = self.font_small.render(f"Herramienta: {self.herramienta}", True, (200, 200, 210))
            self.screen.blit(txt_tool, (ANCHO_PANEL + 14, ALTO - 24))

            pygame.display.flip()
            self.clock.tick(FPS)

# -----------------------------
# Ejecutar
# -----------------------------
if __name__ == "__main__":
    app = GraficadorApp()
    app.run()
