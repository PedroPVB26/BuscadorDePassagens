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


    def formatarHorario(self, horario):
        # Ajeitando "2:20" para "02:20"
        if len(horario) < 5:
            horario = f"0{horario}"

        return horario
    

    def atualizarChegada(self, horario, dataChegada):
        dataChegada += timedelta(int(horario[-1]))

        horario = self.formatarHorario(horario[:-3])

        return horario, dataChegada


    def getHorarios(self, voo, i=0):
        classeHorarios = "lcVysi"
      
        horarios = voo.find_elements(By.CLASS_NAME, classeHorarios)

        dataPartida = datetime.strptime(self.dataAtual, self.formatoDataLink).strftime("%d/%m/%Y")
        dataChegada = datetime.strptime(self.dataAtual,self.formatoDataLink)

        horarioPartida = self.formatarHorario(horarios[0].text)
        horarioChegada = horarios[1].text

        # Avião chega no proximo dia    
        if len(horarioChegada) > 5:
            horarioChegada, dataChegada = self.atualizarChegada(horarioChegada, dataChegada)
        else:
            horarioChegada = self.formatarHorario(horarioChegada)
            
        dataChegada = dataChegada.strftime("%d/%m/%Y")

        partida = f"{dataPartida} : {horarioPartida}"
        chegada = f"{dataChegada} : {horarioChegada}"

        return partida, chegada
    
    
    def getConexoes(self, voo):
        classeConexao = "kwVdvg"

        conexao = voo.find_elements(By.CLASS_NAME, classeConexao)

        if len(conexao) > 1:
            conexao = conexao[1].text[:1]
        else:
            conexao = conexao[0].text[:1]

        if conexao == "D": conexao = "Direto"

        return conexao
