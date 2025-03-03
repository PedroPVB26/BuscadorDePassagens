from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from abc import ABC, abstractmethod

# LATAM: YYYY-MM-DD
# GOL: DD-MM-YYY
# AZUL: DD/MM/YYYY
class Buscador(ABC):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        self.outbound = outbound
        self.origin = origin
        self.destination = destination
        self.intervalo_tempo = intervalo_tempo
        self.preco_maximo = preco_maximo
        self.navegador = navegador
        self.dataDeBusca = datetime.strptime(self.outbound, "%d-%m-%Y")

    def aceitarCookies(self, nome):
        try:
            self.navegador.find_element(By.ID, nome).click()
        except:
            pass
    
    # Serve para pegar o preço já formatado
    @abstractmethod
    def getPreco(self):
        pass

    # Serve para obter a lista que contém os elementos correspondentes aos voos
    @abstractmethod
    def getListaVoos(self):
        pass

    # Deve retornar, por meio de tupla, o horário de partida e chegada
    @abstractmethod
    def getHorarios(self):
        pass

    # Verifica se há conexões, retornando falso se não houver e, se houver, retornando o número de conxeções
    @abstractmethod
    def getConexao(self):
        pass

    # Percorre os voos da lista de voo - Provavelmente o método mais importante
    @abstractmethod
    def pecorrerVoos(self):
        pass
        
    def avancarDataDeBusca(self):
        self.dataDeBusca += timedelta(days=1)


    def atualizarLink(self, link):
        dataAtual = self.dataDeBusca
        self.avancarDataDeBusca()

        ## Se for a primeira vez, ainda terá OUTBOUND no link, caso contrário, tem que atualizar a data anterior de busca pela nova
        if "OUTBOUND" in link:
            return link.replace("OUTBOUND", self.outbound)
            
        else:
            if "latam" in link:
                # Formtar a data para o formato da latam para trocar no link, e atualizar pela proxima data
                dataAtual = dataAtual.strftime("%Y-%m-%d")
            
            elif "gol" in link:
                dataAtual = dataAtual.strftime("%d-%m-%Y")
            
            elif "azul" in link:
                dataAtual = dataAtual.strftime("%d/%m/%Y")

            return link.replace(dataAtual, self.dataDeBusca)
        

    def verificarPreco(self):
        if self.preco_maximo <= self.getPreco():
            return True
        else:
            return False 
