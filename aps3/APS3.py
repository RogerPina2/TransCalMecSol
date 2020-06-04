import numpy as np
import matplotlib.pyplot as plt

L = 0.4

dX = 0.01
dY = dX

nX = int(L/dX) + 1
nY = nX

t = 10
dT = 1e-3
nT = int(t/dT) + 1  

T = np.zeros(shape=(nT,nY,nX))

for e in range(nY):
    T[0][e][0] = 75
    T[0][e][-1] = 50

T[0][0] = 100

k = 0.23
c = 897
p = 2.7

alpha = k/(c*p)

#=====================================

F0 = alpha*(dT/dX**2)
final = -1

for p in range(1,nT):
    tol = 1e-8

    erro = 0
    
    for j in range(nY):
        for i in range(nX):

            if i == 0 or j == 0 or i == (nX-1) or j == (nY-1):
                T[p][j][i] = T[p-1][j][i]
            else:
                T[p][j][i] = F0 * (T[p-1][j][i+1] + T[p-1][j][i-1] + T[p-1][j+1][i] + T[p-1][j-1][i]) + (1 - 4*F0)*T[p-1][j][i]

            if T[p][j][i] != 0:
                aux = abs((T[p][j][i] - T[p-1][j][i])/(T[p][j][i]))
                    
                if aux > erro:
                    erro = aux

    if erro < tol:
        final = p
        break

print('\n'.join([' '.join(['{:8.4f}'.format(item) for item in row]) for row in T[final]]))
print(erro)
print(T[final][20][20])