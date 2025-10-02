import matplotlib.pyplot as plt
import numpy as np
import procesamiento as prot

Imagen1 = plt.imread('imagenes/1.jpg') / 255

fig, axs = plt.subplots(2, 2, figsize=(10, 8))
fig.suptitle("Capas CMYK")

# Capa Cyan
img = prot.ajustarBillo(Imagen1, 0.5)
axs[0, 0].imshow(img)
axs[0, 0].set_title("Brillo general")
axs[0, 0].axis("off")

# ajustar bilbo canal
img = prot.ajustarBilloCanal(Imagen1, 0.5, 1)
axs[0, 1].imshow(img)
axs[0, 1].set_title("brillo canal")
axs[0, 1].axis("off")

#contraste Oscuro
img = prot.aumentarContraste(Imagen1, 0.5, "Oscuro")
axs[1, 0].imshow(img)
axs[1, 0].set_title("contraste Oscuro")
axs[1, 0].axis("off")

#contaste luz

img = prot.aumentarContraste(Imagen1, 0.5, "Luz")
axs[1, 1].imshow(img)
axs[1, 1].set_title("contraste CMYK")
axs[1, 1].axis("off")

plt.tight_layout()
plt.show()


