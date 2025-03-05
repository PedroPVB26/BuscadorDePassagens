# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Tratar para quando não há voos na data

from selenium import webdriver
from buscadorLatam import BuscadorLatam
from buscadorGol import BuscadorGol
from buscadorAzul import BuscadorAzul
import time

navegador = webdriver.Chrome()
navegador.implicitly_wait(10)

# buscadorLatam = BuscadorLatam("05-03-2025", "LDB", "BEL", 4, 5000, navegador)
# buscadorLatam.iniciarBusca()

buscadorGol = BuscadorGol("20-03-2025", "POA", "MAO", 4, 1500, navegador)
buscadorGol.iniciarBusca()

# buscadorAzul = BuscadorAzul("05-03-2025", "LDB", "BEL", 4, 3000, navegador)
# buscadorAzul.iniciarBusca()

time.sleep(30)
