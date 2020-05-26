import numpy as np
import matplotlib.pyplot as plt

k = 0.23
d = 2.7
cp = 897

alpha = k/(cp*d)

L = 0.4 # comprimento do lado da placa em metros

deltaX = 0.1 # espaçamento nodal em metro em X
nnX = int(L/deltaX) + 1 # número de nós na direção X, + 1 pois as duas pontas da barra são nó

deltaY = deltaX # espaçamento nodal em metro em Y
nnY = int(L/deltaY) + 1 # número de nós na direção Y, + 1 pois as duas pontas da barra são nó 

tTotal = 10 # tempo total de análise em segundos
deltaT = 1e-3 # intervalo de tempo entre cada análise em segundos
ni = int(tTotal/deltaT) + 1 # número de intervalos, + 1 para incluir t máximo


M = np.zeros(shape=(ni, nnX, nnY))

for e in range(nnY -1):
    M[0][e][-1] = 50

M[0][0] = 150

def metodo_Diferencas_Finitas(T):

    for l in range(1, ni):
        for i in range(nnX):
            for j in range(nnY):

                F0 = alpha*(deltaT/deltaX**2)

                if i == 0 or i == (nnX-1) or j == (nnY-1):
                    T[l][i][j] = T[l-1][i][j]

                elif j == 0:
                    T[l][i][j] = F0 * (2*T[l-1][i][j+1] + T[l-1][i-1][j] + T[l-1][i+1][j]) + (1 - 4*F0)*T[l-1][i][j]
                
                else:
                    T[l][i][j] = F0 * (T[l-1][i+1][j] + T[l-1][i-1][j] + T[l-1][i][j+1] + T[l-1][i][j-1]) + (1 - 4*F0)*T[l-1][i][j]

metodo_Diferencas_Finitas(M)

for e in M[-1]:
    print(e)

plt.imshow(M[-1])
plt.colorbar()
plt.show()

