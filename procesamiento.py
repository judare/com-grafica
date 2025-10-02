import numpy as np

def procesamiento(Imagen1, Imagen2, factor):
    return (Imagen1 * factor) + (Imagen2 * (1-factor))

def capaRoja(imagen):
    imgC = np.copy(imagen)
    imgC[:,:,1] = imgC[:,:,2] = 0
    return imgC

def capaAzul(imagen):
    imgC = np.copy(imagen)
    imgC[:,:,0] = imgC[:,:,2] = 0
    return imgC

def capaVerde(imagen):
    imgC = np.copy(imagen)
    imgC[:,:,0] = imgC[:,:,1] = 0
    return imgC

def capaAmarillo(imagen):
    imgC = np.copy(imagen)
    imgC[:,:,2] = 0
    return imgC

def capaCyan(imagen):
    imgC = np.copy(imagen)
    imgC[:,:,0] = 0
    return imgC

def capaMagenta(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 1] = 0   # quitamos el canal verde
    return imgC


def capaKey(imagen):
    # Asegurarse que los valores estén en [0,1]
    img = np.copy(imagen)
    R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]

    # Conversión a CMY
    C = 1 - R
    M = 1 - G
    Y = 1 - B

    # Componente K (negro) es el mínimo de los tres
    K = np.minimum(np.minimum(C, M), Y)

    # Imagen en escala de grises
    imgKey = np.zeros_like(img)
    imgKey[:,:,0] = K
    imgKey[:,:,1] = K
    imgKey[:,:,2] = K

    return imgKey


def invertida(imagen):
    return 1 - imagen

def capaGrises(imagen):
    imgC = np.copy(imagen)
    imgC = (imgC[:,:,0] + imgC[:,:,1] + imgC[:,:,2]) / 3
    return imgC

def luminosidad(imagen):
    imgC = np.copy(imagen)
    imgC = (imgC[:,:,0] * 0.299 + imgC[:,:,1] * 0.587 + imgC[:,:,2] * 0.114)
    return imgC

def midgray(imagen):
    imgC = np.copy(imagen)
    imgC = np.maximum(imgC[:,:,0], imgC[:,:,1], imgC[:,:,2]) + np.minimum(imgC[:,:,0], imgC[:,:,1], imgC[:,:,2])
    return imgC

def ajustarBillo (imagen, factor):
    imgC = np.copy(imagen)
    imgC = imgC + factor
    return imgC

def ajustarBilloCanal (imagen, factor, canal):
    imgC = np.copy(imagen)
    imgC[:,:,canal] = imgC[:,:,canal] + factor
    return imgC

def aumentarContraste (imagen, factor, tipo):
    imgC = np.copy(imagen)
    if tipo == "Oscuro":
        imgC =  factor * np.log10(1+imagen)
    else:
        imgC =  factor * np.exp(imagen - 1)
    
    return imgC

def binarizar(imagen, factor):
    imgC = np.copy(imagen)
    imgC = (imgC[:,:,0] + imgC[:,:,1] + imgC[:,:,2]) / 3
    U = imgC > factor
    return U

def zoom(imagen, factorZoom, areaZoom, w, h):
    imgC = np.copy(imagen)
    imgC = imgC[areaZoom[0]:areaZoom[1], areaZoom[2]:areaZoom[3]]
    
    zoomed = np.kron(imgC, np.ones((factorZoom, factorZoom, 1)))
    return zoomed

def termica(imagen, TemMin, TemMax, NBits):
    imgC = np.copy(imagen)

    GradosC = (TemMax-TemMin)*imgC/2**NBits+TemMin

    