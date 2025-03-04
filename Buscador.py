from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import time
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

    
    # # Serve para pegar o preço já formatado
    # @abstractmethod
    def getPreco(self):
        pass


    # # Serve para obter a lista que contém os elementos correspondentes aos voos
    @abstractmethod
    def getListaVoos(self):
        pass


    # # Deve retornar, por meio de tupla, o horário de partida e chegada
    # @abstractmethod
    # def getHorarios(self):
    #     pass


    # # Verifica se há conexões, retornando falso se não houver e, se houver, retornando o número de conxeções
    # @abstractmethod
    # def getConexao(self):
    #     pass


    # # Percorre os voos da lista de voo - Provavelmente o método mais importante
    # @abstractmethod
    # def pecorrerVoos(self):
    #     pass
        
    @abstractmethod
    def aceitarCookies(self):
        pass

    def avancarDataDeBusca(self):
        self.dataDeBusca += timedelta(days=1)

    @abstractmethod
    def atualizarLink(self):
        pass

    # def atualizarLink(self, link):
    #     dataAtual = self.dataDeBusca
    #     self.avancarDataDeBusca()

    #     # Caso seja a primeira vez, o link ainda não conterá as informações necessárias.
    #     if "OUTBOUND" and "ORIGIN" in link:
    #         if "latam" in link:
    #             # Formtar a data para o formato da latam para trocar no link, e atualizar pela proxima data
    #             self.outbound = dataAtual.strftime("%Y-%m-%d")
            
    #         elif "gol" in link:
    #             self.outbound = dataAtual.strftime("%d-%m-%Y")
            
    #         elif "azul" in link:
    #             self.outbound = dataAtual.strftime("%d/%m/%Y")
        
    #         self.link = link.replace("OUTBOUND", self.outbound)
    #         self.link = self.link.replace("ORIGIN", self.origin)
    #         self.link = self.link.replace("DESTINATION", self.destination)

    #     else:
    #         if "latam" in link:
    #             # Formtar a data para o formato da latam para trocar no link, e atualizar pela proxima data
    #             dataAtual = dataAtual.strftime("%Y-%m-%d")
            
    #         elif "gol" in link:
    #             dataAtual = dataAtual.strftime("%d-%m-%Y")
            
    #         elif "azul" in link:
    #             dataAtual = dataAtual.strftime("%d/%m/%Y")

    #         self.link = link.replace(dataAtual, self.dataDeBusca)
        

    def verificarPreco(self):
        if self.preco_maximo <= self.getPreco():
            return True
        else:
            return False 
        

    def verificarTamanhoLista(self, lista):
        x = 0
        for elemento in lista:
            x+=1

        print(x)

    def iniciarBusca(self):
        # 1 Entrar no link
        self.atualizarLink()
        self.navegador.get(self.link)

        # 2 Aceitar Cookies
        # Não esquecer de esperar a página carregar
        self.aceitarCookies()

        # 3 Pegar a lista de Voos
        listaVoos = self.getListaVoos()
        self.verificarTamanhoLista(listaVoos)
        # 4 Percorrer os voos
        for voo in listaVoos:
            
        # 5 Pegar as informações dos voos
            # 5.1 Pegar Preco
            preco = self.getPreco(voo)
            print(preco)

            # 5.2 Pegar Datas e Horários (Partida e Chegada)


            # 5.3 Pegar Conexões

        # 5.4 Salvar as informações em uma tabela

        # 5.5 Ir para a próxima data de voos e recomeçar a partir do item 3
        
