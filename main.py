# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Tratar para quando não há voos na data

from Aeroportos import CadastroAeroporto
from BuscadorLatam import BuscadorLatam
from BuscadorAzul import BuscadorAzul
from BuscadorGol import BuscadorGol
from Janela import Janela
from selenium import webdriver
import pandas as pd
import os

# Lista dos aeroportos
ca = CadastroAeroporto("Aeroportos.json")
ca.verificarExistênciaArquivo()
listaAeroportos = ca.getListaAeroportos()


# Interface Gráfica - Janela
janela = Janela(listaAeroportos)
janela.mainloop()


# Pegando as variáveis de ambiente criadas pela janela
outbound = os.getenv('OUTBOUND')
inbound = os.getenv('INBOUND')
origin = os.getenv('ORIGIN')
destination = os.getenv('DESTINATION')
precoMaximo = float(os.getenv('PRECO_MAXIMO'))
email = os.getenv('EMAIL')
diferenca = int(os.getenv('DIFERENCA'))


# Inicializando o navegador
navegador = webdriver.Chrome()
navegador.implicitly_wait(10)


# ---------- LATAM ----------
buscadorLatam = BuscadorLatam(outbound, origin, destination, diferenca, precoMaximo ,navegador)
tabLatam = buscadorLatam.iniciarBusca()


# ---------- GOL ----------
buscadorGol = BuscadorGol(outbound, origin, destination, diferenca, precoMaximo ,navegador)
tabGol = buscadorGol.iniciarBusca()


# ---------- AZUL ----------
buscadorAzul = BuscadorAzul(outbound, origin, destination, diferenca, precoMaximo ,navegador)
tabAzul = buscadorAzul.iniciarBusca()


# Formatando a Tabela
tabelaVoos = pd.concat([tabLatam, tabGol, tabAzul])
tabelaVoos = tabelaVoos.sort_values('Preço')

print(tabelaVoos.columns)

# Formatando a data
tabelaVoos['Partida']  = pd.to_datetime(tabelaVoos['Partida'], format = "%d/%m/%Y - %H:%M")
tabelaVoos['Chegada'] = pd.to_datetime(tabelaVoos['Chegada'], format = "%d/%m/%Y - %H:%M")

tabelaVoos['Partida'] = tabelaVoos['Partida'].dt.strftime("%H:%M - %d/%m")
tabelaVoos['Chegada'] = tabelaVoos['Chegada'].dt.strftime("%H:%M - %d/%m")

# Salvando a tabela
tabelaVoos.to_excel('Voos.xlsx', index=False)

