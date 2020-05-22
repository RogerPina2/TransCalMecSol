# Discretização de diferenças finitas 
    # determinar a distribuição de temperatura
        # barra de alumínio
            # L = 50 cm
            # dimensões desprezíveis em relação ao eixo = unidimensional

'''
    Para a discretização do domínio use
    uma malha uniforme com
    espaçamento de 5 cm no
    comprimento da barra e 5s em
    relação ao tempo.
'''

import numpy as np
import matplotlib.pyplot as plt

alpha = 1/(100*100) #m^2

L = 0.5 # comprimento da barra em metros
deltaX = 0.05 # espaçamento nodal em metro
nn = int(L/deltaX) + 1 # número de nós, + 1 pois as duas pontas da barra são nó

tTotal = 500 #+ 20*8 # tempo total de análise
deltaT = 5 # intervalo de tempo entre cada análise
ni = int(tTotal/deltaT) + 1 # número de intervalos, + 1 para incluir t = 500

# cria uma matriz T (malha temporal) sendo:
#   nn (número de nós) = quantidade de linhas
#       cada linha representa um ponto do nó
#   ni (número de intervalos) = quantidade de colunas
#       cada coluna representa um intervalo de tempo
T = np.zeros(shape=(nn, ni))

# Condição inicial da barra
#   todos os pontos no interior da barra = 20ºC, enquanto q as pontas = 0ºC
for e in range(1, nn-1):
    T[e][0] = 20


def metodo_Diferencas_Finitas(T):
    """
        Método das diferenças finitas - unidimensional
        Eq. nos slides da aula 18
    """
    # Utilizamos l e i para respeitar a equação dos slides
    for l in range(1, ni):
        for i in range(1, nn-1):

            # A única diferença é que calculamos para l ao invés de l+1, isso fará que l seja l-1
            T[i][l] = T[i][l-1] + (alpha*(deltaT/deltaX**2))*(T[i+1][l-1] - 2*T[i][l-1] + T[i-1][l-1])

metodo_Diferencas_Finitas(T)

# O intervalo delta X é uma lista que representa o comprimento da barra divida em intervalos de deltaX
ideltaX = np.linspace(0, L, 11, endpoint=True)

# plot de todas análises de temperatura
# a análise é feita a cada 5s
# cada coluna da matriz T representa uma análise
for l in range(ni):
    # a função np.column_stack(MATRIZ)[IDX] transforma a coluna de valor IDX da MATRIZ em uma lista
    plt.plot(ideltaX, np.column_stack(T)[l])
plt.show()

print(np.column_stack(T)[-1])
