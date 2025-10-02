import matplotlib.pyplot as plt
import numpy as np
import procesamiento as prot

Imagen1 = plt.imread('imagenes/1.jpg') / 255

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Capas CMYK")


img = prot.invertida(Imagen1 )
axs[0, 0].imshow(img)
axs[0, 0].set_title("Invertida")
axs[0, 0].axis("off")

img = prot.capaGrises(Imagen1)
axs[0, 1].imshow(img, cmap="gray")
axs[0, 1].set_title("Escala grises")
axs[0, 0].axis("off")


img = prot.capaGrises(Imagen1)
axs[1, 0].imshow(img, cmap="gray")
axs[1, 0].set_title("Luminosidad")
axs[0, 0].axis("off")

img = prot.midgray(Imagen1)
axs[1, 1].imshow(img, cmap="gray")
axs[1, 1].set_title("midgray")
axs[0, 0].axis("off")

plt.tight_layout()
plt.show()


