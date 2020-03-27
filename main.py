import src.funcoesTermosol as ft
from src.metodoIterativo import metodoInterativo

import numpy as np

# nn = numero de nós
# N = matriz de nós
# nm = numero de membros
# Inc = matriz de incidencia
# nc = numero de cargas
# F = vetor carregamento
# nr = numero de restricoes
# R = vetor com os graus de liberdade restritos
[nn,N,nm,Inc,nc,F,nr,R] = ft.importa('src/entrada.xlsx')
ft.plota(N,Inc)

# ===================================== DESLOCAMENTO NODAL ==========================================
def deslocamentoNodal(nn, N, nm, Inc, F, R):
    """
        nn = numero de nós
        N = matriz de nós
        nm = numero de membros
        Inc = matriz de incidencia
        F = vetor carregamento
        R = vetor com os graus de liberdade restritos
    """

    K = []
    # cria uma matriz de rigidez pra cada elemento e alva em K
    for elemento in range(nm):
        nos = Inc[elemento][0:2]

        no1 = int(nos[0])
        no2 = int(nos[1])

        no1x = N[0][no1 - 1]
        no1y = N[1][no1 - 1]

        no2x = N[0][no2 - 1]
        no2y = N[1][no2 - 1]

        l = ((no2x - no1x)**2 + (no2y - no1y)**2)**(1/2)
        E = Inc[elemento][2]
        A = Inc[elemento][3]

        # cria Matriz de senos e cossenos
        k = ((E * A) / l) 

        s = (no2y - no1y)/l
        c = (no2x - no1x)/l

        matriz = np.array([ [  c**2 ,   c*s  , -(c**2), -c*s  ],
                            [  c*s  ,   s**2 , -c*s  , -(s**2)],
                            [-(c**2),   -c*s ,  c**2 ,   c*s  ],
                            [  -c*s , -(s**2),  c*s  ,  s**2  ]])

        Ke = k * matriz

        K.append(Ke)

    # Faz a Superposicao de Matrizes e salva em Kg
    Kg = np.zeros((nn*2,nn*2))

    idxGdlK = []
    for elemento in range(len(Inc)):
        no1 = int(Inc[elemento][0])
        no2 = int(Inc[elemento][1])
        
        idxGdlKe = [(no1-1)*2, (no1-1)*2 + 1, (no2-1)*2, (no2-1)*2 + 1]
        idxGdlK.append(idxGdlKe)
    
    for e in range(len(K)):
        idx = idxGdlK[e]

        for i in range(4):
            for j in range(4):
                Kg[idx[i]][idx[j]] += K[e][i][j]
    
    KgSalvo = np.array(Kg)

    # Utiliza Kg pro metodo iterativo
    P = np.array(F)

    for e in range(len(R)): 
        Kg = np.delete(Kg,int(R[-1-e]), 0)
        Kg = np.delete(Kg,int(R[-1-e]), 1)
        P  = np.delete(P, int(R[-1-e]), 0)

    U = metodoInterativo(10000, 10e-16, Kg, P)

    Ufinal = np.zeros((nn*2,1))

    cont = 0
    for e in range(len(Ufinal)):
        if e not in R:
            Ufinal[e] = U[cont]
            cont +=1

    return Ufinal, KgSalvo

# ===================================== REAÇÕES DE APOIO ==========================================

def reacoesDeApoio(nc, F, nr, R, U, Kg):
    P = np.matmul(Kg,U)

    for e in range(nr):
        R[e]

'''
def getAngulo(no1, no2, N):
    import math

    no1x = N[0][no1 - 1]
    no1y = N[1][no1 - 1]

    no2x = N[0][no2 - 1]
    no2y = N[1][no2 - 1]

    # calcular o coef. ang. do elemento
    m = 0
    if no2x - no1x != 0: m = (no2y - no1y)/(no2x - no1x)

    # coeficiente angular do elemento
    ang = math.atan(m)

    return ang

def calculaForçaPerpendicular(no1, no2, N, F):
    import math 

    ang = getAngulo(no1,no2,N)

    no1F = F[(no1-1)*2]*math.cos(ang) + F[(no1*2)-1]*math.sin(ang)
    no2F = F[(no2-1)*2]*math.cos(ang) + F[(no2*2)-1]*math.sin(ang)

    forca = abs(no1F - no2F)

    return forca

def tensaoNoElemento(Inc, F, N):
    tensoes = []
    for e in range(len(Inc)):
        no1 = int(Inc[e][0])
        no2 = int(Inc[e][1])    
        
        P = calculaForçaPerpendicular(no1, no2, N, F)
        A = Inc[e][3]
        tensao = P/A
        tensoes.append(tensao)

    return tensoes
    
def deformacaoLongitudinal(Inc, F, N):
    deformacoes = []
    for e in range(len(Inc)):
        nos = Inc[e][0:2]    
        
        no1 = int(nos[0])
        no2 = int(nos[1])

        no1x = N[0][no1 - 1]
        no1y = N[1][no1 - 1]

        no2x = N[0][no2 - 1]
        no2y = N[1][no2 - 1]

        l = ((no2x - no1x)**2 + (no2y - no1y)**2)**(1/2)
        P = calculaForçaPerpendicular(no1, no2, N, F)
        A = Inc[e][3]
        E = Inc[e][2]

        deformacao = (P * l)/(A * E)
        deformacoes.append(deformacao)

        print('Elem.' + str(e), 'nós', Inc[e][0:2], 'Deformação =', deformacao)

    return deformacoes



def getSinCos(N, nos, l):
    no1 = int(nos[x mi0])
    no2 = int(nos[1])

    no1x = N[0][no1 - 1]
    no1y = N[1][no1 - 1]

    no2x = N[0][no2 - 1]
    no2y = N[1][no2 - 1]

    s = (no2y - no1y)/l
    c = (no2x - no1x)/l

    return s,c

def tensao(nm, Inc, U):
    tensao = np.zeros(nm)
    Ut = np.zeros(4)
    for elemento in range(nm):
        nos = Inc[elemento][0:2]
        
        l = getComprimento(N, nos)
        E = Inc[elemento][2]
        k = E/l

        s,c = getSinCos(N, nos, l)

        mat = np.array([-c, -s, c, s])

        cont = 0
        for e in nos:
            e = (int(e)-1)*2
            Ut[cont] = U[e]
            Ut[cont+1] = U[e+1]

        ts = k*mat*Ut

        print(ts)
'''
#Ti = tensaoNoElemento(Inc, F, N)
#deformacaoLongitudinal(Inc,F,N)

U, Kg = deslocamentoNodal(nn, N, nm, Inc, F, R)
reacoesDeApoio(nc, F, nr, R, U, Kg)
#tensao(nm, Inc, U)


#ft.geraSaida('saída',1,U,1,1,1)