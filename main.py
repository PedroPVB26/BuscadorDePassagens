# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Tratar para quando não há voos na data

from selenium import webdriver
from BuscadorLatam import BuscadorLatam
from BuscadorGol import BuscadorGol
from BuscadorAzul import BuscadorAzul
import time

navegador = webdriver.Chrome()
navegador.implicitly_wait(10)

buscadorLatam = BuscadorLatam("17-04-2025", "BEL", "LDB", 2, 5000, navegador)
buscadorLatam.iniciarBusca()

# buscadorGol = BuscadorGol("21-03-2025", "BEL", "STM", 2, 1500, navegador)
# buscadorGol.iniciarBusca()

# buscadorAzul = BuscadorAzul("14-03-2025", "LDB", "VCP", 2, 3000, navegador)
# buscadorAzul.iniciarBusca()

# time.sleep(30)
