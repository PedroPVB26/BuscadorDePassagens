# https://medium.com/@guilhermerdcarvalho/paradigma-orientado-ao-objeto-poo-em-python-a107d35bee3f

# Verificar se é viável fazer a função atualizarLink na classe Buscador

from selenium import webdriver
from buscadorLatam import BuscadorLatam
from buscadorGol import BuscadorGol
from buscadorAzul import BuscadorAzul


navegador = webdriver.Chrome()
navegador.implicitly_wait(10)

# buscadorLatam = BuscadorLatam("20-03-2025", "LDB", "BEL", 4, 1500, navegador)
# buscadorLatam.iniciarBusca()

# buscadorGol = BuscadorGol("20-03-2025", "LDB", "BEL", 4, 1500, navegador)
# buscadorGol.iniciarBusca()

buscadorAzul = BuscadorAzul("05-03-2025", "LDB", "BEL", 4, 3000, navegador)
buscadorAzul.iniciarBusca()
