import numpy as np
import matplotlib.pyplot as plt

alpha = 0.25 #m^2/s

L = 0.5 # comprimento do lado da placa em metros

deltaX = 0.1 # espaçamento nodal em metro em X
nnX = int(L/deltaX) + 1 # número de nós na direção X, + 1 pois as duas pontas da barra são nó

deltaY = deltaX # espaçamento nodal em metro em Y
nnY = int(L/deltaY) + 1 # número de nós na direção Y, + 1 pois as duas pontas da barra são nó 

tTotal = 10 # tempo total de análise em segundos
deltaT = 10e-2 # intervalo de tempo entre cada análise em segundos
ni = int(tTotal/deltaT) + 1 # número de intervalos, + 1 para incluir t máximo

# cria uma matriz T (malha temporal de temperatura) sendo:
#   nnX (número de nós em X) = quantidade de linhas
#   nnY (número de nós em Y) = quantidade de colunas
#       cada valor da matriz representa um nó
#   ni (número de intervalos) = quantidade de matrizes
#       cada matriz representa um intervalo de tempo
T = np.zeros(shape=(ni, nnX, nnY))

# ============= Condição inicial da placa ============= 
#   todos os pontos no interior da placa = 0ºC
#   enquanto que os lados = 100ºC, 0ºC, 0ºC, 0ºC (cima, direita, baixo, esquerda)

T[0][0] = 100



def metodo_Diferencas_Finitas(T):
    """
        Método das diferenças finitas - bidimensional
        Eq. nos slides da aula 19
    """
    # Utilizamos l e i para respeitar a equação dos slides
    for l in range(1, ni):
        for i in range(nnX):
            for j in range(nnY):

                if i == 0 or j == 0 or i == (nnX-1) or j == (nnY-1):
                    T[l][i][j] = T[l-1][i][j]
                else:
                    T[l][i][j] = T[l-1][i][j] + (alpha*(deltaT/deltaX**2))*((T[l-1][i+1][j] - 2*T[l-1][i][j] + T[l-1][i-1][j]) + (T[l-1][i][j+1] - 2*T[l-1][i][j] + T[l-1][i][j-1]))


metodo_Diferencas_Finitas(T)

'''
plt.plot(T[0])
plt.show()
'''
'''
plt.imshow(T[-1])
plt.colorbar()
plt.show()

'''

print(T[3])

