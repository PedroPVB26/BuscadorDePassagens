from Buscador import Buscador
from selenium.webdriver.common.by import By
import time
from datetime import datetime, timedelta


class BuscadorAzul(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
        self.link = "https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds=ORIGIN&c[0].std=OUTBOUND&c[0].as=DESTINATION&p[0].t=ADT&p[0].c=1&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL&1741034666867"
        self.formatoDataLink = "%m/%d/%Y"
        self.idCookie = "onetrust-accept-btn-handler"


    def getPreco(self, voo):
        classePreco = "current"

        try:
            preco = voo.find_element(By.CLASS_NAME, classePreco).text[2:]
            preco = preco.replace(".", "").replace(",",".")
            return float(preco)
        except:
            print("Azul - Não foi possível pegar o preço")


    # Exibir todos os voos
    def pressionarBtnVerMaisVoos(self):
        idBotao = "load-more-button"

        try:
            btnVerMaisVoos = self.navegador.find_element(By.ID, idBotao)

            while True:
                if btnVerMaisVoos:
                    try:
                        self.navegador.execute_script("arguments[0].scrollIntoView(true);", btnVerMaisVoos)
                        time.sleep(1)
                        btnVerMaisVoos.click()
                    except:
                        break
                else:
                    break        
        except:
            pass

    # Pegar somente os voos não esgotados
    # A verificação é feita pela existência do preço da passagem no voo
    def deletarVoosEsgotados(self, listaVoosOriginal):
        classePreco = "current"
        novaListaVoos = []

        for voo in listaVoosOriginal:
            try:
                voo.find_element(By.CLASS_NAME, classePreco).text # Se tem preço, não tá esgotado
                novaListaVoos.append(voo)
            except:
                pass
        return novaListaVoos
        

    def getListaVoos(self):
        classeVoos = "flight-card" #-> Esta classe pega ate os voos esgotados

        self.pressionarBtnVerMaisVoos()

        try:
            listaVoos = self.navegador.find_elements(By.CLASS_NAME, classeVoos)
            listaVoos = self.deletarVoosEsgotados(listaVoos)
            return listaVoos
        except:
            print("AZUL - Não foi possível pegar a lista dos voos")


    def atualizarChegada(self, dataPartida, horarioChegada):  # Pensar na lógica para quando o voo não necessariamente chegar no próximo dia, ou chegar no outro ano
        if(len(horarioChegada) > 9):
            dataPartida = datetime.strptime(dataPartida, "%d/%m/%Y")
            dataPartida += timedelta(days=1)
            dataPartida = dataPartida.strftime("%d/%m/%Y")
            horarioChegada = horarioChegada[:5]
        else:
            horarioChegada = horarioChegada[:5]

        return horarioChegada, dataPartida
    

    def getHorarios(self, voo, i=0):
        classePartida = "departure"
        classeChegada = "arrival"
        # classeDatas = "iata-day"

        dataPartida = datetime.strptime(self.dataAtual, self.formatoDataLink).strftime("%d/%m/%Y") 

        horarioPartida = voo.find_element(By.CLASS_NAME, classePartida).text[:5]
        horarioChegada = voo.find_element(By.CLASS_NAME, classeChegada).text

        horarioChegada, dataChegada = self.atualizarChegada(dataPartida, horarioChegada)
        
        partida = f"{dataPartida} : {horarioPartida}"
        chegada = f"{dataChegada} : {horarioChegada}"

        return partida, chegada
    
    def getConexoes(self, voo, i=0):
        classeConexao = "flight-leg-info"

        conexao = voo.find_element(By.CLASS_NAME, classeConexao).text

        if "D" in conexao: 
            conexao = "Direto"
        else:
            conexao = conexao[:1]

        return conexao
