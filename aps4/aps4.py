import numpy as np
import matplotlib.pyplot as plt

# Lados do retângulo
Lx = 30
Ly = 30

# Delta X e Delta Y
dX = 0.5
dY = dX

# nº de nós na direção X e Y
nX = int(Lx/dX) + 1
nY = int(Ly/dY) + 1 

# Tempo total e tempo de despejo
Tt = 5
Td = 2

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
Q = 80

# Valores de u e v
u = 1
v = 0

# Valores de a e b
a = 15
b = 15

# Index dos pontos a e b
idxA = int(nX*a/Lx)
idxB = int(nY*b/Ly)

for t in range(nT):
    for y in range(nY):
        for x in range(nX):

            if x == 0:
                C[t][y][x] = C[t][y][x+1]

            elif x == nX-1:
                C[t][y][x] = C[t][y][x-1]

            elif y == 0:
                C[t][y][x] = C[t][y+1][x]

            elif y == nY-1:
                C[t][y][x] = C[t][y-1][x]
            
            else:
                pK = K/dX**2 * (C[t-1][y][x+1] + C[t-1][y][x-1] + C[t-1][y+1][x] + C[t-1][y-1][x] - 4*C[t-1][y][x])
                pU = (u/(2*dX)) * (C[t-1][y][x+1] - C[t-1][y][x-1])
                pV = (v/(2*dX)) * (C[t-1][y+1][x] - C[t-1][y-1][x])

                if t < nD and x == idxA and y == idxB:
                    pQ = Q/dX**2
                    C[t][y][x] = ( pQ + pK - pU - pV) * dT + C[t-1][y][x]
                
                else:
                    pQ = 0
                    C[t][y][x] = ( pQ + pK - pU - pV) * dT + C[t-1][y][x]

print(C[-1][40][40])

plt.imshow(C[-1])
plt.colorbar()
plt.show()