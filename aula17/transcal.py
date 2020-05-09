import numpy as np
from math import *

#determinar as dimensões da aleta
k = 200 #W/mK - material (cond. term. do mat.)
L = 300/1000 #m - comprimento 
lado = 30/1000 #m - comp. lado
tb = 350 #K - temp. base
ta = 300 #K - temp. ambie.
h = 15 #W/m^2K - coef. de troca term.


#determinar a taxa de transf. de calor
m = ((h*(4*lado))/(k*(lado**2)))**(1/2)

#Determinar a distribuição de temperatura ao longo da aleta.

lista_temp = []
lista_comp = np.linspace(0, L, 100, endpoint=True)


def distTemp_transfCalorConv(x):
    return (cosh(m*(L-x)) + (h/(m*k)) * sinh(m*(L-x)))/(cosh(m*L)+(h/(m*k))*sinh(m*L)) 


tetab = tb - ta

for e in lista_comp:
    lista_temp.append((distTemp_transfCalorConv(e) * tetab) + ta)

import matplotlib.pyplot as plt

plt.plot(lista_comp, lista_temp)
plt.show()

for e in range(len(lista_comp)):
    menor = 1
    idx = 0
    if abs((L/2) - lista_comp[e]) < menor:
        menor = abs((L/2) - lista_comp[e])
        idx = e

print(lista_temp[idx])