from Buscador import Buscador
from selenium.webdriver.common.by import By

class BuscadorGol(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
            super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
            self.link = "https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de=LDB&para=BEL&ida=23-04-2025&ADT=1&CHD=0&INF=0&voebiz=0"
            self.formatoDataLink = "%d-%m-%Y"
            self.idCookie = "onetrust-accept-btn-handlerA"


    def getPreco(self, voo):
        classePreco = "a-desc__value--price"
        try:
            preco = voo.find_element(By.CLASS_NAME, classePreco).text[3:]
            preco = preco.replace(".", "").replace(",",".")
            return float(preco)
        except:
            print("GOL - Não foi possível pegar o preço")


    def getListaVoos(self):
        classeVoos = "p-select-flight__accordion"
        try:
            return self.navegador.find_elements(By.CLASS_NAME, classeVoos)
        except:
            print("GOL - Não foi possível pegar a lista dos voos")