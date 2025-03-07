from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from abc import ABC, abstractmethod
import pandas as pd


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
        self.listaVoosEncontrados = {
            'Empresa' : [],
            'Partida': [],
            'Chegada': [],
            'Conexões': [],
            'Preço': [],
            'Link': [],
        }
    
    
    # # Serve para pegar o preço já formatado
    @abstractmethod
    def getPreco(self, voo):
        pass


    # # Serve para obter a lista que contém os elementos correspondentes aos voos
    @abstractmethod
    def getListaVoos(self):
        pass


    # # Deve retornar, por meio de tupla, o horário de partida e chegada
    @abstractmethod
    def getHorarios(self, voo, i):
        pass

    
    # def excluirVoosEsgotados(self):
    #     pass

    # # Verifica se há conexões, retornando falso se não houver e, se houver, retornando o número de conxeções
    @abstractmethod
    def getConexoes(self, voo, i):
        pass


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
        dataAnterior = self.dataAtual  
        self.dataAtual = self.proxDataDeBusca
        self.avancarProxDataDeBusca()
            
        # Se for a primeira busca, ou seja, o link ainda não foi atualizado
        if "OUTBOUND" in self.link:
            self.dataAtual = self.dataAtual.strftime(self.formatoDataLink)
            self.link = self.link.replace("OUTBOUND", self.dataAtual)
            self.link = self.link.replace("ORIGIN", self.origin)
            self.link = self.link.replace("DESTINATION", self.destination)
        else:
            self.link = self.link.replace(dataAnterior, self.dataAtual.strftime(self.formatoDataLink))
            self.dataAtual = self.dataAtual.strftime(self.formatoDataLink)            

        
    def verificarPreco(self, preco):
        if preco <= self.preco_maximo:
            return True
        else:
            return False 
        

    def verificarTamanhoLista(self, lista):
        print(len(lista))


    def iniciarBusca(self):
        for it in range(self.intervalo_tempo):
            # 1 Entrar no link
            self.atualizarLink()
            self.navegador.get(self.link)

            # 2 Aceitar Cookies
            # Não esquecer de esperar a página carregar
            self.aceitarCookies()

            # 3 Pegar a lista de Voos
            listaVoos = self.getListaVoos()
            
            # 4 Percorrer os voos
            for i, voo in enumerate(listaVoos):
                preco = self.getPreco(voo)

            # 5 Pegando as Informações dos voos
                if self.verificarPreco(preco):
                    partida, chegada = self.getHorarios(voo, i)
                    conexao = self.getConexoes(voo, i)

                    self.listaVoosEncontrados['Empresa'].append(self.__class__.__name__[8:].upper())
                    self.listaVoosEncontrados['Partida'].append(partida)
                    self.listaVoosEncontrados['Chegada'].append(chegada)
                    self.listaVoosEncontrados['Conexões'].append(conexao)
                    self.listaVoosEncontrados['Preço'].append(preco)
                    self.listaVoosEncontrados['Link'].append(self.link)

        
        return pd.DataFrame(self.listaVoosEncontrados)
