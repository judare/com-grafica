


import matplotlib.pyplot as plt
import numpy as np
import procesamiento as prot


plt.figure("Fusion")

plt.subplot(1,3,1)
Imagen1 = plt.imread('imagenes/1.jpg')/255
plt.imshow(Imagen1)
plt.axis('off')
# plt.show()

plt.subplot(1,3,2)
plt.figure("Bloque")
Imagen2 = plt.imread('imagenes/2.jpg')/255
plt.imshow(Imagen2)
plt.axis('off')
# plt.show()

plt.subplot(1,3,3)
plt.figure("Imagenes fusionadas")
imgFusionada = prot.procesamiento(Imagen1, Imagen2, 0.5)
plt.imshow(imgFusionada)
plt.axis('off')
plt.show()