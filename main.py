# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Finalizar a função de pegar a lista de voos da Azul

from selenium import webdriver
from buscadorLatam import BuscadorLatam
from buscadorGol import BuscadorGol
from buscadorAzul import BuscadorAzul
import time

navegador = webdriver.Chrome()
navegador.implicitly_wait(10)

# buscadorLatam = BuscadorLatam("20-03-2025", "LDB", "BEL", 4, 1500, navegador)
# buscadorLatam.iniciarBusca()

# buscadorGol = BuscadorGol("20-03-2025", "LDB", "BEL", 4, 1500, navegador)
# buscadorGol.iniciarBusca()

buscadorAzul = BuscadorAzul("22-03-2025", "LDB", "BEL", 4, 1500, navegador)
buscadorAzul.iniciarBusca()

time.sleep(30)