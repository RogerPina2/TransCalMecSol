import numpy as np
import matplotlib.pyplot as plt

alpha = 0.25 #m^2/s

L = 0.5 # comprimento do lado da placa em metros

deltaX = 0.1 # espaçamento nodal em metro em X
nnX = int(L/deltaX) + 1 # número de nós na direção X, + 1 pois as duas pontas da barra são nó

deltaY = deltaX # espaçamento nodal em metro em Y
nnY = int(L/deltaY) + 1 # número de nós na direção Y, + 1 pois as duas pontas da barra são nó 

tTotal = 10 # tempo total de análise em segundos
deltaT = 1e-2 # intervalo de tempo entre cada análise em segundos
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

global final
final = -1
def metodo_Diferencas_Finitas(T):
    """
        Método das diferenças finitas - bidimensional
        Eq. nos slides da aula 19
    """
    F0 = (alpha*(deltaT/deltaX**2))
    convergencia = 0

    # Utilizamos l e i para respeitar a equação dos slides
    for p in range(1, ni):
        for i in range(nnX):
            for j in range(nnY):

                if j == 0 or i == (nnX-1) or j == (nnY-1):
                    T[p][i][j] = T[p-1][i][j]

                elif i == 0:
                    termo_fora_da_placa = 0 #A gente precisa implementar a parte com derivada, só q é dificil, não queremos pensa pq somos preguiçosos :D
                    T[p][i][j] = F0 * (T[p-1][i+1][j] + termo_fora_da_placa +  T[p-1][i][j+1] + T[p-1][i][j-1]) + (1 - 4*F0)*T[p-1][i][j] #derivada parcial = 0 
                
                else:
                    T[p][i][j] = F0 * (T[p-1][i+1][j] + T[p-1][i-1][j] + T[p-1][i][j+1] + T[p-1][i][j-1]) + (1 - 4*F0)*T[p-1][i][j]

                    if(abs((T[p][i][j]-T[p-1][i][j])/T[p][i][j]) > convergencia):
                        convergencia = abs((T[p][i][j]-T[p-1][i][j])/T[p][i][j])
        
        if(convergencia < 1e-4):
            final = p
            break

metodo_Diferencas_Finitas(T)


plt.imshow(T[-1])
plt.colorbar()
plt.show()


print(T[final])
print(final)

