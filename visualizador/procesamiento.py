import numpy as np

def procesamiento(Imagen1, Imagen2, factor):
    return (Imagen1 * factor) + (Imagen2 * (1-factor))


def capaRoja(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 1] = 0
    imgC[:, :, 2] = 0
    return imgC

def capaAzul(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0
    imgC[:, :, 1] = 0
    return imgC

def capaVerde(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0
    imgC[:, :, 2] = 0
    return imgC

def capaAmarillo(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 2] = 0  # B = 0
    return imgC

def capaCyan(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 0] = 0  # R = 0
    return imgC

def capaMagenta(imagen):
    imgC = np.copy(imagen)
    imgC[:, :, 1] = 0  # G = 0
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

    
def procesamiento(Imagen1, Imagen2, factor):
    """Funde dos imágenes con un factor de transparencia."""
    # Asegurarse de que las imágenes tengan el mismo tamaño
    h1, w1, _ = Imagen1.shape
    h2, w2, _ = Imagen2.shape
    if h1 != h2 or w1 != w2:
        img2_pil = Image.fromarray((Imagen2 * 255).astype(np.uint8))
        img2_resized = img2_pil.resize((w1, h1))
        Imagen2 = np.array(img2_resized) / 255.0
        
    return (Imagen1 * factor) + (Imagen2 * (1 - factor))


def invertida(imagen):
    """Calcula el negativo de la imagen."""
    return 1.0 - imagen

def ajustarBrillo(imagen, factor):
    """Ajusta el brillo de la imagen."""
    imgC = np.clip(imagen + factor, 0.0, 1.0)
    return imgC

def aumentarContraste(imagen, factor):
    """Ajusta el contraste de la imagen."""
    imgC = np.clip(128 + factor * (imagen * 255 - 128), 0, 255) / 255.0
    return imgC

def binarizar(imagen, factor):
    """Convierte la imagen a blanco y negro usando un umbral."""
    imgC = np.copy(imagen)
    gris = (imgC[:, :, 0] * 0.299 + imgC[:, :, 1] * 0.587 + imgC[:, :, 2] * 0.114)
    binaria = (gris > factor).astype(float)
    return np.stack([binaria] * 3, axis=-1)
    
def rotar_imagen(imagen, angulo):
    """Rota la imagen un ángulo determinado."""
    from PIL import Image
    img_pil = Image.fromarray((imagen * 255).astype(np.uint8))
    img_rotada = img_pil.rotate(angulo, expand=True, fillcolor='black')
    return np.array(img_rotada) / 255.0
