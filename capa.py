import matplotlib.pyplot as plt
import numpy as np
import procesamiento as prot

Imagen1 = plt.imread('imagenes/1.jpg') / 255

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Capas CMYK")

# Capa Cyan
imgCyan = prot.capaCyan(Imagen1)
axs[0, 0].imshow(imgCyan)
axs[0, 0].set_title("Cyan")
axs[0, 0].axis("off")

# Capa Magenta
imgMagenta = prot.capaMagenta(Imagen1)
axs[0, 1].imshow(imgMagenta)
axs[0, 1].set_title("Magenta")
axs[0, 1].axis("off")

# Capa Yellow
imgYellow = prot.capaAmarillo(Imagen1)
axs[1, 0].imshow(imgYellow)
axs[1, 0].set_title("Yellow")
axs[1, 0].axis("off")

# Capa Key (Negro)
imgKey = prot.capaKey(Imagen1)
axs[1, 1].imshow(imgKey, cmap="gray")
axs[1, 1].set_title("Key (Black)")
axs[1, 1].axis("off")

plt.tight_layout()
plt.show()


