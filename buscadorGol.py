from Buscador import Buscador
from selenium.webdriver.common.by import By

class BuscadorGol(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
            super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
            self.link = "https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de=LDB&para=BEL&ida=23-04-2025&ADT=1&CHD=0&INF=0&voebiz=0"

    def atualizarLink(self):
        dataAtual = self.dataDeBusca
        self.avancarDataDeBusca()
            
        # Se for a primeira busca, ou seja, o link ainda não foi atualizado
        if "OUTBOUND" in self.link:
            dataAtual = dataAtual.strftime("%d-%m-%Y")
            self.link = self.link.replace("OUTBOUND", dataAtual)
            self.link = self.link.replace("ORIGIN", self.origin)
            self.link = self.link.replace("DESTINATION", self.destination)
        else:
            self.link = self.link.replace(dataAtual.strftime("%d-%m-%Y"), self.dataDeBusca.strftime("%d-%m-%Y"))
          

    def aceitarCookies(self):
        idCookie = "onetrust-accept-btn-handler"
        try:
            self.navegador.find_element(By.ID, idCookie).click()
        except:
            print("GOL - Não foi possível clicar no botão de aceitar os Cookies")


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