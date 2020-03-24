
import numpy as np

def metodoInterativo(ite, tol, K, F):
    #Saídas: U, Erro associado

    U = []
    for e in range(len(K)):
        U.append(0.0)

    Unew = np.array(U)
    i = 0
    while i < ite:
        Uold = np.array(Unew)
        for e in range(len(Uold)):          
            Unew[e] = F[e]

            for f in range(len(Uold) - 1): 
                c = e+f+1                   
                if c >= len(Uold):          
                    c -= len(Uold)          

                Unew[e] -= (K[e][c] * Unew[c])

            Unew[e] /= K[e][e]

        if i > 1:
            erros = ((Unew - Uold)/Uold) * 100

            maior = erros[0]
            for erro in erros:
                if erro > maior:
                    maior = erro

            if maior < tol:
                break
            
        i+= 1

    print("foram " + str(i) + " iterações")

    return Unew

'''
k = np.array([[1.59, -0.4, -0.54], [-0.4, 1.7, 0.4], [-0.54, 0.4, 0.54]])
print(k)
K = 10e8 * k
F = np.array([0, 150, -100])

print(metodoInterativo(10000, 10e-16, K, F))

k = np.array([[1.0,-1.0], [-1.0,1.0]])
K = ((0.02*200e9)/2) * k
F = np.array([50000.0, 0])

print(metodoInterativo(100000, 10e-16, K, F))
'''