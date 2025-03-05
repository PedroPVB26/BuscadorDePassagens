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
        self.proxDataDeBusca = datetime.strptime(self.outbound, "%d-%m-%Y")
        self.dataAtual = self.proxDataDeBusca
    
    
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
    def getHorarios(self):
        pass

    
    def excluirVoosEsgotados(self):
        pass

    # # Verifica se há conexões, retornando falso se não houver e, se houver, retornando o número de conxeções
    # @abstractmethod
    # def getConexao(self):
    #     pass


    # # Percorre os voos da lista de voo - Provavelmente o método mais importante
    # @abstractmethod
    # def pecorrerVoos(self):
    #     pass
        
    def aceitarCookies(self):
        try:
            self.navegador.find_element(By.ID, self.idCookie).click()
        except:
            print(f"{self.__class__.__name__} - Erro ao aceitar os Cookies || Cookies já foram aceitos")


    def avancarProxDataDeBusca(self):
        self.proxDataDeBusca += timedelta(days=1)


    def atualizarLink(self):
        self.dataAtual = self.proxDataDeBusca
        self.avancarProxDataDeBusca()
            
        # Se for a primeira busca, ou seja, o link ainda não foi atualizado
        if "OUTBOUND" in self.link:
            self.dataAtual = self.dataAtual.strftime(self.formatoDataLink)
            self.link = self.link.replace("OUTBOUND", self.dataAtual)
            self.link = self.link.replace("ORIGIN", self.origin)
            self.link = self.link.replace("DESTINATION", self.destination)
        else:
            self.link = self.link.replace(self.dataAtual.strftime(self.formatoDataLink), self.proxDataDeBusca.strftime(self.formatoDataLink))


    def verificarPreco(self, preco):
        if preco <= self.preco_maximo:
            return True
        else:
            return False 
        

    def verificarTamanhoLista(self, lista):
        print(len(lista))


    def iniciarBusca(self):
        # 1 Entrar no link
        self.atualizarLink()
        self.navegador.get(self.link)

        # 2 Aceitar Cookies
        # Não esquecer de esperar a página carregar
        self.aceitarCookies()

        # 3 Pegar a lista de Voos
        listaVoos = self.getListaVoos()
        
        # 4 Percorrer os voos
        for voo in listaVoos:
            preco = self.getPreco(voo)

            if self.verificarPreco(preco):
                print(preco)
            else:
                print("Preço da passagem é superior ao desejado")            
            
        # 5 Pegar as informações dos voos
            # 5.1 Pegar Preco


            # 5.2 Pegar Datas e Horários (Partida e Chegada)
            self.getHorarios(voo)

            # 5.3 Pegar Conexões

        # 5.4 Salvar as informações em uma tabela

        # 5.5 Ir para a próxima data de voos e recomeçar a partir do item 3
        
