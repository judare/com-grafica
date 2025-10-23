import pygame

# --- Definición del algoritmo DDA (de la imagen 2) ---
def dda(screen, x1, y1, x2, y2, color):
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

# --- Código principal de Pygame (de la imagen 1) ---

# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
running = True
Linea = False

# Inicializar coordenadas
xIni, yIni = 0, 0
xFin, yFin = 0, 0

# fill the screen with a color to wipe away anything from last frame
# (Lo dejamos fuera del bucle como en tu imagen, las líneas se acumularán)
screen.fill("white")

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Hacer click", event.pos)
            xIni = event.pos[0]
            yIni = event.pos[1]

        if event.type == pygame.MOUSEBUTTONUP:
            print("Soltar click", event.pos)
            xFin = event.pos[0]
            yFin = event.pos[1]
            Linea = True # Activa la bandera para dibujar

    # RENDER YOUR GAME HERE

    # Si la bandera Linea es Verdadera, dibuja la línea USANDO DDA
    if Linea:
        # --- AQUÍ ES EL CAMBIO ---
        # En lugar de: pygame.draw.line(screen,"Black",(xIni,yIni),(xFin,yFin),1)
        # Usamos la función dda:
        dda(screen, xIni, yIni, xFin, yFin, "Black")
        # ------------------------
        
        Linea = False # Resetea la bandera para no dibujarla en cada frame

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()