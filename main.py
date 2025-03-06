# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Tratar para quando não há voos na data

from selenium import webdriver
from BuscadorLatam import BuscadorLatam
from BuscadorGol import BuscadorGol
from BuscadorAzul import BuscadorAzul
import time

navegador = webdriver.Chrome()
navegador.implicitly_wait(10)

buscadorLatam = BuscadorLatam("17-04-2025", "BEL", "MAO", 4, 5000, navegador)
buscadorLatam.iniciarBusca()

# buscadorGol = BuscadorGol("20-03-2025", "POA", "MAO", 4, 1500, navegador)
# buscadorGol.iniciarBusca()

# buscadorAzul = BuscadorAzul("14-03-2025", "LDB", "BEL", 4, 3000, navegador)
# buscadorAzul.iniciarBusca()

time.sleep(30)
