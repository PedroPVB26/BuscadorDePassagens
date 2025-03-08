# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Tratar para quando não há voos na data

from Aeroportos import CadastroAeroporto
from BuscadorLatam import BuscadorLatam
from BuscadorAzul import BuscadorAzul
from BuscadorGol import BuscadorGol
from selenium import webdriver
import pandas as pd

ca = CadastroAeroporto("Aeroportos.json")
ca.verificarExistênciaArquivo()

# navegador = webdriver.Chrome()
# navegador.implicitly_wait(10)

# # ---------- LATAM ----------
# buscadorLatam = BuscadorLatam("17-04-2025", "BEL", "LDB", 2, 1500, navegador)
# tabLatam = buscadorLatam.iniciarBusca()


# # ---------- GOL ----------
# buscadorGol = BuscadorGol("21-03-2025", "BEL", "STM", 2, 1500, navegador)
# tabGol = buscadorGol.iniciarBusca()


# # ---------- AZUL ----------
# buscadorAzul = BuscadorAzul("14-03-2025", "LDB", "VCP", 2, 3000, navegador)
# tabAzul = buscadorAzul.iniciarBusca()


# # Formatando a Tabela
# tabelaVoos = pd.concat([tabLatam, tabGol, tabAzul])
# tabelaVoos = tabelaVoos.sort_values('Preço')

# print(tabelaVoos.columns)

# # Formatando a data
# tabelaVoos['Partida']  = pd.to_datetime(tabelaVoos['Partida'], format = "%d/%m/%Y - %H:%M")
# tabelaVoos['Chegada'] = pd.to_datetime(tabelaVoos['Chegada'], format = "%d/%m/%Y - %H:%M")

# tabelaVoos['Partida'] = tabelaVoos['Partida'].dt.strftime("%H:%M - %d/%m")
# tabelaVoos['Chegada'] = tabelaVoos['Chegada'].dt.strftime("%H:%M - %d/%m")

# # Salvando a tabela
# tabelaVoos.to_excel('Voos.xlsx', index=False)

