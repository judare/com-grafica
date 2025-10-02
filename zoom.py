import matplotlib.pyplot as plt
import numpy as np
import procesamiento as prot

Imagen1 = plt.imread('imagenes/1.jpg') / 255

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Capas CMYK")



# Capa Magenta
imgMagenta = prot.zoom(Imagen1, 5, (0, Imagen1.shape[0], 0, Imagen1.shape[1]), Imagen1.shape[0], Imagen1.shape[1])
axs[0, 1].imshow(imgMagenta)
axs[0, 1].set_title("Magenta")
axs[0, 1].axis("off")

plt.tight_layout()
plt.show()


