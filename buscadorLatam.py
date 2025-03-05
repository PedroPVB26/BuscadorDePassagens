from Buscador import Buscador
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

class BuscadorLatam(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
        self.link = "https://www.latamairlines.com/br/pt/oferta-voos/?origin=ORIGIN&outbound=OUTBOUNDT12%3A00%3A00.000Z&destination=DESTINATION&inbound=null&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"
        self.formatoDataLink = "%Y-%m-%d"
        self.idCookie = "cookies-politics-button"


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


    def getHorarios(self, voo):
        classeHorarios = "lcVysi"
      
        horarios = voo.find_elements(By.CLASS_NAME, classeHorarios)

        dataPartida = datetime.strptime(self.dataAtual,"%Y-%m-%d").strftime("%d/%m/%Y")
        dataChegada = datetime.strptime(self.dataAtual,"%Y-%m-%d")
