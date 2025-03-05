from Buscador import Buscador
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta

class BuscadorGol(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
        self.link = "https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de=ORIGIN&para=DESTINATION&ida=OUTBOUND&ADT=1&CHD=0&INF=0&voebiz=0"
        self.formatoDataLink = "%d-%m-%Y"
        self.idCookie = "onetrust-accept-btn-handler"


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


    def atualizarChegada(self, horaPartida, horaChegada, dataChegada):
        if int(horaChegada[:2]) < int(horaPartida[:2]):
            dataChegada += timedelta(days=1) # Pensar na lógica para quando o voo não necessariamente chegar no próximo dia

        return dataChegada.strftime("%d/%m/%Y")
    

    def getHorarios(self, voo, i):
        idHorarioPar = f"lbl_origin_{i + 1}_emission"
        idHorarioChe = f"lbl_destination_{i + 1}_emission"

        dataPartida = datetime.strptime(self.dataAtual, self.formatoDataLink).strftime("%d/%m/%Y")
        dataChegada = datetime.strptime(self.dataAtual, self.formatoDataLink)

        horarioPartida = voo.find_element(By.ID, idHorarioPar).text[6:]
        horarioChegada = voo.find_element(By.ID, idHorarioChe).text[6:]

        dataChegada = self.atualizarChegada(horarioPartida, horarioChegada, dataChegada)

        partida = f"{dataPartida} : {horarioPartida}"
        chegada = f"{dataChegada} : {horarioChegada}"

        print(f"{partida} - {chegada}")

        return partida, chegada