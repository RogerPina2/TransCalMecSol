import numpy as np
import matplotlib.pyplot as plt
import math
import time

# Lados do retângulo
Lx = 30
Ly = 20

# Delta X e Delta Y
dX = 0.5
dY = dX

# nº de nós na direção X e Y
nX = int(Lx/dX) + 1
nY = int(Ly/dY) + 1 

# Tempo total e tempo de despejo
Tt = 30
Td = 3

# Intervalo entre cada análise
dT = 0.05

# Número total de análises no intervalo de tempo total
# Número total de análises no intervalo de tempo de despejo
nT = int(Tt/dT) + 1
nD = int(Td/dT) + 1

# Matriz
C = np.zeros(shape=(nT,nY,nX))

# Valores de K e Q
K = 1
Q = 100

# Valores de u e v
alpha = 1
u = alpha

# Valores de a e b
a = int(8/1.4)
b = int(60/(8+5))

# Index dos pontos a e b
idxA = int(nX*a/Lx)
idxB = int(nY*b/Ly)

final = -1

for t in range(nT):
    for y in range(1,nY-1):
        for x in range(1,nX-1):
            
            v = alpha * math.sin((math.pi/5) * (x*dX))

            pK = (K/dX**2) * (C[t-1][y][x+1] + C[t-1][y][x-1] + C[t-1][y+1][x] + C[t-1][y-1][x] - 4*C[t-1][y][x])
            pU = (u/(2*dX)) * (C[t-1][y][x+1] - C[t-1][y][x-1])
            pV = (v/(2*dX)) * (C[t-1][y+1][x] - C[t-1][y-1][x])

            if t < nD and x == idxA and y == idxB:
                pQ = Q/dX**2
                C[t][y][x] = ( pQ + pK - pU - pV) * dT + C[t-1][y][x]
                
            else:
                pQ = 0
                C[t][y][x] = ( pQ + pK - pU - pV) * dT + C[t-1][y][x]
  
    C[t][0][:] = C[t][1][:]
    C[t][-1][:] = C[t][-2][:]
    C[t][:][0] = C[t][:][1]
    #C[t][:][-1] = C[t][:][-2]

    for e in range(nY):
        C[t][e][-1] = C[t][e][-2]

plt.imshow(C[0])
plt.gca().invert_yaxis()
plt.colorbar()
plt.show()

plt.imshow(C[1])
plt.gca().invert_yaxis()
plt.colorbar()
plt.show()

plt.imshow(C[2])
plt.gca().invert_yaxis()
plt.colorbar()
plt.show()
