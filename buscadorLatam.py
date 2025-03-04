# Para a Latam, eu pecorro por meio dos botões, porém, os seus IDs podem mudar, mas pelo Link não. Então fazer uma busca igual a da Gol, por meio dos Links
from Buscador import Buscador
from selenium.webdriver.common.by import By
import time

class BuscadorLatam(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
        self.link = "https://www.latamairlines.com/br/pt/oferta-voos/?origin=ORIGIN&outbound=OUTBOUNDT12%3A00%3A00.000Z&destination=DESTINATION&inbound=null&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"

    
    def atualizarLink(self):
        dataAtual = self.dataDeBusca
        self.avancarDataDeBusca()
            
        # Se for a primeira busca, ou seja, o link ainda não foi atualizado
        if "OUTBOUND" in self.link:
            dataAtual = dataAtual.strftime("%Y-%m-%d")
            self.link = self.link.replace("OUTBOUND", dataAtual)
            self.link = self.link.replace("ORIGIN", self.origin)
            self.link = self.link.replace("DESTINATION", self.destination)
        else:
            self.link = self.link.replace(dataAtual.strftime("%Y-%m-%d"), self.dataDeBusca.strftime("%Y-%m-%d"))


    def aceitarCookies(self):
        idCookie = "cookies-politics-button"
        try:
            self.navegador.find_element(By.ID, idCookie).click()
        except:
            print("LATAM - Não foi possível clicar no botão de aceitar os Cookies")


    def getPreco(self, voo):
        classePreco = "koxMWe"
        try:
            preco = voo.find_elements(By.CLASS_NAME, classePreco)[1].text[4:]
            preco = preco.replace(".", "").replace(",",".")
            return float(preco)
        except:
            print("LATAM - Não foi possível pegar o preço")


    def getListaVoos(self):
        classeVoos = "ciAabv"
        try:
            return self.navegador.find_elements(By.CLASS_NAME, classeVoos)
        except:
            print("LATAM - Não foi possível pegar a lista dos voos")


