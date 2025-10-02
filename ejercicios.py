


import matplotlib.pyplot as plt
import numpy as np


plt.figure("Matriz")

def ejercicio1():
    M = np.zeros((3,3,3))

    # cmyl
    M[0,0] = [0,1,1] # cyan
    M[1,0] = [1,0,1] # magenta
    M[2,0] = [1,1,0] # amarillo

    # grises
    M[0,1] = [1,1,1] # blanco
    M[1,1] = [0.5,0.5,0.5] # gris
    M[2,1] = [0,0,0] # negro

    # rgb
    M[0,2] = [1,0,0] # rojo
    M[1,2] = [0,1,0] # verde
    M[2,2] = [0,0,1] # azul


    plt.imshow(M)
    plt.show()

def ejercicio2(N, N2):
    M = np.zeros((N,N2,3))
    # grises

    M[0:9,0] = [1,1,0] # amarillo
    M[0:9,1:3] = [0,1,1] # cyan
    M[0:9,3:5] = [0,1,0] # verde
    M[0:9,5:7] =[1,0,1] # magenta

    M[0:9,7:9] = [1,0,0] # rojo
    M[0:9,9:11] = [0,0,1] # azul

    for i in range(0,N):
        M[N-1, i] = [i/N,i/N,i/N] # gris
        M[N-2,  i] = [i/N,i/N,i/N] # gris

    plt.imshow(M)
    plt.show()

def gradiente(M):
    Ma = np.zeros((M,M,3))
    for i in range(0,M):
        for j in range(0,M):
            for k in range(0,3):
                Ma[i,j] =  [k/3,j/M, i/M ]
                # Ma[i,j, k] = (j/M + i/M) * k 

    plt.imshow(Ma)
    plt.show()


gradiente(10)