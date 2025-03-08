import requests
import json
import os

# Essa classe é responsável por pegar os aeroportos do Brasil via api e armazenar em um dicionário
# O dicionário é utilizado para que o usuário possa escolher os aeroportos de origem e destino


class CadastroAeroporto:
    def __init__(self, nomeArquivoAeroportos):
        self.nomeArquivoAeroportos = nomeArquivoAeroportos


    def criarArquivoAeroportos(self):
        aeroportos = []
        with open(self.nomeArquivoAeroportos, "w") as f:
            json.dump(aeroportos,f)        


    def getListaAeroportos(self):
        with open(self.nomeArquivoAeroportos, "r") as f:
            return json.load(f)
            

    def verificarExistênciaArquivo(self):
        try:
            with open(self.nomeArquivoAeroportos, "r") as f:
                json.load(f)
        except:
            self.criarArquivoAeroportos()
            self.buscarAeroportos("br")
            

    def buscarAeroportos(self, country):
        lista = []
        page = 1
        while True:
            apiUrl = f"https://sharpapi.com/api/v1/airports?page={page}&per_page=100&country={country}"
            response = requests.get(apiUrl, headers = {"Authorization": f"Bearer {os.environ['apiKey']}", "Accept": "application/json"})

            if response.status_code == requests.codes.ok:
                aeroportos = response.json()

                if aeroportos:
                    for aeroporto in aeroportos['data']:
                        iata = aeroporto['iata']
                        nomeAeroporto = aeroporto['name']
                        cidade = aeroporto['city']   

                        if iata and cidade:
                            lista.append([cidade, nomeAeroporto, iata])    
                else:
                    break
            else:
                break
            page += 10
            
        lista = sorted(lista, key=lambda x: x[0])

        # Armazena a lista no arquivo .json de forma ordenado
        with open(self.nomeArquivoAeroportos, 'w') as f:
            json.dump(lista, f)