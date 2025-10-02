import numpy as np
import matplotlib.pyplot as plt

# Cargar imagen TIFF
ImagenTiff = np.array(plt.imread("imagenes/t1.tiff"))
D = np.double(ImagenTiff)

# Parámetros de temperatura
TemMin = -40
TemMax = 160
NBits = 14

# Conversión a grados centígrados
MatrizCenti = np.array((TemMax - TemMin) * D / (2**NBits) + TemMin)

filas, columnas = MatrizCenti.shape

# Inicializar valores
temp_min = float("inf")
temp_max = float("-inf")
temp_mediana = np.median(MatrizCenti)

coord_min = (-1, -1)
coord_max = (-1, -1)
coord_mediana = (-1, -1)

# Recorrer toda la matriz
for i in range(filas):
    for j in range(columnas):
        valor = MatrizCenti[i, j]

        if valor < temp_min:
            temp_min = valor
            coord_min = (i, j)

        if valor > temp_max:
            temp_max = valor
            coord_max = (i, j)

        if coord_mediana == (-1, -1) or abs(valor - temp_mediana) < abs(MatrizCenti[coord_mediana] - temp_mediana):
            coord_mediana = (i, j)

print("Coordenadas mínima:", coord_min, "valor:", temp_min)
print("Coordenadas máxima:", coord_max, "valor:", temp_max)
print("Coordenadas mediana:", coord_mediana, "valor:", MatrizCenti[coord_mediana])

# ---- Graficar en una sola figura con subplots ----
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# Imagen termográfica
im = axes[0].imshow(MatrizCenti, cmap=plt.cm.hot_r)
axes[0].set_title("Imagen Termográfica")
fig.colorbar(im, ax=axes[0], shrink=0.8)

# Marcar el punto máximo con un círculo magenta
circle = plt.Circle((coord_max[1], coord_max[0]), radius=10, color='magenta', fill=True, linewidth=2)
axes[0].add_patch(circle)

# Marcar el punto mínimo con un círculo rojo
circle = plt.Circle((coord_min[1], coord_min[0]), radius=10, color='cyan', fill=True, linewidth=2)
axes[0].add_patch(circle)

# Histograma
hist, bins = np.histogram(MatrizCenti, np.arange(0, TemMax), density=True)
HistoTempeBar = np.int32(MatrizCenti.round())
axes[1].hist(HistoTempeBar, 5, facecolor='red', alpha=0.5)
axes[1].set_title("Histograma")

plt.tight_layout()
plt.show()
