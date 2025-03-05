from Buscador import Buscador
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
import time

class BuscadorAzul(Buscador):
    def __init__(self, outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
        super().__init__(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
        self.link = "https://www.voeazul.com.br/br/pt/home/selecao-voo?c[0].ds=ORIGIN&c[0].std=OUTBOUND&c[0].as=DESTINATION&p[0].t=ADT&p[0].c=1&p[0].cp=false&f.dl=3&f.dr=3&cc=BRL&1741034666867"
        self.formatoDataLink = "%m/%d/%Y"
        self.idCookie = "onetrust-accept-btn-handler"


    def getPreco(self, voo):
        print("--- getPreco ---")
        classePreco = "current"

        try:
            preco = voo.find_element(By.CLASS_NAME, classePreco).text[2:]
            preco = preco.replace(".", "").replace(",",".")
            return float(preco)
        except:
            print("Azul - Não foi possível pegar o preço")


    # Exibir todos os voos
    def pressionarBtnVerMaisVoos(self):
        print("--- pressionarBtnVerMaisVoos ---")
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

    # Pegar somente os voos não esgotados
    # A verificação é feita pela existência do preço da passagem no voo
    def deletarVoosEsgotados(self, listaVoosOriginal):
        print("--- deletarVoosEsgotados ---")
        classePreco = "current"
        novaListaVoos = []

        for voo in listaVoosOriginal:
            print("--- verificandoVoo ---")
            try:
                voo.find_element(By.CLASS_NAME, classePreco).text # Se tem preço, não tá esgotado
                novaListaVoos.append(voo)
            except:
                pass
        return novaListaVoos
        

    def getListaVoos(self):
        print("--- getListaVoos ---")
        classeVoos = "flight-card" #-> Esta classe pega ate os voos esgotados

        self.pressionarBtnVerMaisVoos()

        try:
            listaVoos = self.navegador.find_elements(By.CLASS_NAME, classeVoos)
            listaVoos = self.deletarVoosEsgotados(listaVoos)
            return listaVoos
        except:
            print("AZUL - Não foi possível pegar a lista dos voos")