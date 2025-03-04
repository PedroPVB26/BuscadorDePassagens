from Buscador import Buscador
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

class BuscadorAzul(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
            super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
            self.link = "https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds=ORIGIN&c[0].std=OUTBOUND&c[0].as=DESTINATION&p[0].t=ADT&p[0].c=1&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL&1741034666867"

    def atualizarLink(self):
        dataAtual = self.dataDeBusca
        self.avancarDataDeBusca()
            
        # Se for a primeira busca, ou seja, o link ainda não foi atualizado
        if "OUTBOUND" in self.link:
            dataAtual = dataAtual.strftime("%m/%d/%Y")
            self.link = self.link.replace("OUTBOUND", dataAtual)
            self.link = self.link.replace("ORIGIN", self.origin)
            self.link = self.link.replace("DESTINATION", self.destination)
        else:
            self.link = self.link.replace(dataAtual.strftime("%m/%d/%Y"), self.dataDeBusca.strftime("%m/%d/%Y"))


    def aceitarCookies(self):
        idCookie = "onetrust-accept-btn-handler"
        try:
            self.navegador.find_element(By.ID, idCookie).click()
        except:
            print("AZUL - Não foi possível clicar no botão de aceitar os Cookies")


    def getPreco(self, voo):
        classePreco = "current"
        # TRATAR PARA O CASO DOS VOOS ESGOTADOS
        try:
            preco = voo.find_element(By.CLASS_NAME, classePreco).text[2:]
            preco = preco.replace(".", "").replace(",",".")
            return float(preco)
        except:
            print("Azul - Não foi possível pegar o preço")


    def pressionarBtnVerMaisVoos(self):
        idBotao = "load-more-button"
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

    def getListaVoos(self):
        classeVoos = "flight-card" #-> Esta classe pega ate os voos esgotados. Avaliar posteriormente o que fazer (informar que os há voos esgotados?)
        # classeVoos = "css-1txam" -> Não pega o primeiro voo

        # Antes de Pegar a lista efetivamente, tem que ficar apertando no botão "Ver mais voos", que fica no final da página, até que ele desapareça 
        self.pressionarBtnVerMaisVoos()
            
        try:
            return self.navegador.find_elements(By.CLASS_NAME, classeVoos)
        except:
            print("AZUL - Não foi possível pegar a lista dos voos")