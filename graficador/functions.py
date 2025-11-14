import pygame



def plot(surface, color, x, y):
    """
    Dibuja un "píxel" en el canvas.
    Usamos circle con radio 1 (como en el DDA original)
    para que sea visible y más rápido que set_at().
    """
    pygame.draw.circle(surface, color, (round(x), round(y)), 1)


def dda(surface, color, pos1, pos2):
    """Algoritmo DDA (Digital Differential Analyzer) para líneas."""
    x1, y1 = pos1
    x2, y2 = pos2
    dx = x2 - x1
    dy = y2 - y1

    if abs(dx) > abs(dy):
        steps = int(abs(dx))
    else:
        steps = int(abs(dy))

    if steps == 0:
        plot(surface, color, x1, y1)
        return

    x_inc = dx / steps
    y_inc = dy / steps
    x, y = x1, y1

    for _ in range(steps + 1):
        plot(surface, color, x, y)
        x += x_inc
        y += y_inc


def bresenham_line(surface, color, pos1, pos2):
    """Algoritmo de línea de Bresenham."""
    x1, y1 = int(pos1[0]), int(pos1[1])
    x2, y2 = int(pos2[0]), int(pos2[1])
    
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    
    # Pendiente
    err = dx - dy

    while True:
        plot(surface, color, x1, y1)
        if x1 == x2 and y1 == y2:
            break
        
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy


def bresenham_circle(surface, color, center, radius):
    """Algoritmo de círculo de Bresenham."""
    if radius <= 0:
        return
    xc, yc = int(center[0]), int(center[1])
    x, y = 0, int(radius)
    d = 3 - 2 * int(radius)

    def plot_octants(xc, yc, x, y):
        plot(surface, color, xc + x, yc + y)
        plot(surface, color, xc - x, yc + y)
        plot(surface, color, xc + x, yc - y)
        plot(surface, color, xc - x, yc - y)
        plot(surface, color, xc + y, yc + x)
        plot(surface, color, xc - y, yc + x)
        plot(surface, color, xc + y, yc - x)
        plot(surface, color, xc - y, yc - x)

    plot_octants(xc, yc, x, y)
    while y >= x:
        x += 1
        if d > 0:
            y -= 1
            d = d + 4 * (x - y) + 10
        else:
            d = d + 4 * x + 6
        plot_octants(xc, yc, x, y)


def midpoint_ellipse(surface, color, center, rx, ry):
    """Algoritmo de elipse de punto medio."""
    if rx <= 0 or ry <= 0:
        return
    
    xc, yc = int(center[0]), int(center[1])
    rx, ry = int(rx), int(ry)

    rx2 = rx * rx
    ry2 = ry * ry
    two_rx2 = 2 * rx2
    two_ry2 = 2 * ry2

    def plot_quadrants(x, y):
        plot(surface, color, xc + x, yc + y)
        plot(surface, color, xc - x, yc + y)
        plot(surface, color, xc + x, yc - y)
        plot(surface, color, xc - x, yc - y)

    # Región 1
    x = 0
    y = ry
    p = round(ry2 - rx2 * ry + 0.25 * rx2)
    
    px = 0
    py = two_rx2 * y

    plot_quadrants(x, y)

    while px < py:
        x += 1
        px += two_ry2
        if p < 0:
            p += ry2 + px
        else:
            y -= 1
            py -= two_rx2
            p += ry2 + px - py
        plot_quadrants(x, y)

    # Región 2
    p = round(ry2 * (x + 0.5)**2 + rx2 * (y - 1)**2 - rx2 * ry2)
    
    while y >= 0:
        y -= 1
        py -= two_rx2
        if p > 0:
            p += rx2 - py
        else:
            x += 1
            px += two_ry2
            p += rx2 - py + px
        plot_quadrants(x, y)


def bezier_curve(surface, color, p0, p1, p2, p3, steps=50):
    """Dibuja una curva de Bézier cúbica (4 puntos)."""
    
    def get_bezier_point(t, p0, p1, p2, p3):
        # Fórmula de Bernstein
        u = 1 - t
        u2 = u * u
        u3 = u2 * u
        t2 = t * t
        t3 = t2 * t
        
        x = u3*p0[0] + 3*u2*t*p1[0] + 3*u*t2*p2[0] + t3*p3[0]
        y = u3*p0[1] + 3*u2*t*p1[1] + 3*u*t2*p2[1] + t3*p3[1]
        return (x, y)

    last_pos = p0
    for i in range(1, steps + 1):
        t = i / steps
        current_pos = get_bezier_point(t, p0, p1, p2, p3)
        # Dibujamos segmentos de línea (DDA) entre los puntos interpolados
        dda(surface, color, last_pos, current_pos)
        last_pos = current_pos

