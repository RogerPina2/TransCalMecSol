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
<<<<<<< HEAD:aps1/main.py
[nn,N,nm,Inc,nc,F,nr,R] = ft.importa('src/input/entrada.xlsx')
=======
[nn,N,nm,Inc,nc,F,nr,R] = ft.importa('src/input/aula10-6.xlsx')
>>>>>>> master:main.py
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
    # cria uma matriz de rigidez pra cada elemento e salva em K
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

    U = metodoInterativo(10000, 10e-16, Kg, P, 1)

    Ufinal = np.zeros((nn*2,1))

    cont = 0
    for e in range(len(Ufinal)):
        if e not in R:
            Ufinal[e] = U[cont]
            cont +=1

    return Ufinal, KgSalvo

# ===================================== REAÇÕES DE APOIO ==========================================

def reacoesDeApoio(F, nr, R, U, Kg):
    F = np.matmul(Kg,U)

    reacoes = np.zeros((nr,1))
    for e in range(nr):
        reacoes[e] = F[int(R[e])]        

    return reacoes

# ===================================== DEFORMAÇÕES ==========================================

def deformacoes(nn, N, nm, Inc, U):

    deformacoes = np.zeros((nm,1))

    for elemento in range(nm):
        nos = Inc[elemento][0:2]

        no1 = int(nos[0])
        no2 = int(nos[1])

        no1x = N[0][no1 - 1]
        no1y = N[1][no1 - 1]

        no2x = N[0][no2 - 1]
        no2y = N[1][no2 - 1]

        l = ((no2x - no1x)**2 + (no2y - no1y)**2)**(1/2)

        #seno e cosseno
        s = (no2y - no1y)/l
        c = (no2x - no1x)/l

        u = np.array([U[(no1-1)*2], U[(no1-1)*2+1], U[(no2-1)*2], U[(no2-1)*2 + 1]])
        
        matSinCos = np.array([-c, -s, c, s])
        
        deformacao = 1/l * np.matmul(matSinCos,u)

        deformacoes[elemento] = deformacao

    return deformacoes

# ===================================== TENSÕES INTERNAS ==========================================

def tensoes(nm, Inc, Epsi):
    """
        Calcula as tensões dos elementos.
        nm = numero de elementos
        Inc = matriz de Incidência
        Epsi = deformação de cada elemento
    """
    
    tensoes = np.zeros((nm,1))

    for elemento in range(nm):
        E = Inc[elemento][2]        
        tensao = E * Epsi[elemento]
        tensoes[elemento] = tensao

    return tensoes

# ===================================== FORÇAS INTERNAS ==========================================

def forcasInternas(nm, Inc, Ti):
    Finternas = np.zeros((nm,1))
    
    for elemento in range(nm):
        tensao = Ti[elemento]
        area = Inc[elemento][3]
        Finterna = tensao*area
        Finternas[elemento] = Finterna
    
    return Finternas

# =================================================================================

U, Kg = deslocamentoNodal(nn, N, nm, Inc, F, R)
Ft = reacoesDeApoio(F, nr, R, U, Kg)
Epsi = deformacoes(nn, N, nm, Inc, U)
Ti = tensoes(nm, Inc, Epsi)
Fi = forcasInternas(nm, Inc, Ti)

<<<<<<< HEAD:aps1/main.py
ft.geraSaida('saída', Ft, U, Epsi, Fi, Ti)
=======
ft.geraSaida('saída-Aula10-6', Ft, U, Epsi, Fi, Ti)
>>>>>>> master:main.py
