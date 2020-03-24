import src.funcoesTermosol as ft
from src.metodoIterativo import metodoInterativo

[nn,N,nm,Inc,nc,F,nr,R] = ft.importa('src/entrada.xlsx')
ft.plota(N,Inc)