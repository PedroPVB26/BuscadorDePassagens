![alt text](hand-holding-plane-sky.jpg)

# Buscador de Passagens
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Selenium](https://img.shields.io/badge/-selenium-%43B02A?style=for-the-badge&logo=selenium&logoColor=white)
![Google Chrome](https://img.shields.io/badge/Google%20Chrome-4285F4?style=for-the-badge&logo=GoogleChrome&logoColor=white)

## O que é?
Um sistema que busca passagens para um período, pega as que estiverem na faixa de preço informado e envia as informações dos voos encontrados para o email informado.

## Requisitos
- Para que o sistema funcione corretamente, é necessária a instalação de:
    - **Git**
        - Necessário para a clonagem do repositório
        - [Instalar Git](https://git-scm.com/)

    - **Python**
        - O sistema foi feito em python, portanto é necessário tê-lo para a execução do sistema
        - Baixe a versão mais atual
        - [Instalar Python](https://www.python.org/downloads/)

    - **ChromeDriver**
        - Verifique a versão do seu Google Chrome e baixe a versão do Chromedrive correspondente a ela;
        - Para verificar a versão do seu Chrome, vá em chrome://settings/help.
        - [Instalar ChromeDrivee](https://developer.chrome.com/docs/chromedriver/downloads?hl=pt-br)

    - **Google Chrome**
        - Por hora, o sistema foi feito para roda apenas no Chrome
        - [Instalar Google Chrome]((https://support.google.com/chrome/answer/95346?hl=pt-BR&co=GENIE.Platform%3DDesktop#zippy=%2Cwindows))

## Como funciona
### 1 - Informações necessárias:
- **Data de Início e Final**: O sistema permite buscar passagens para múltiplos dias. Para isso, o usuário deve informar a data de início, que marca o primeiro dia do período desejado, e a data final, que define o último dia. Com essas informações, o sistema pesquisa todas as passagens disponíveis dentro desse intervalo.

- **Origem**: é o aeroporto de origem, de onde o voo irá partir.

- **Destino**: é o aeroporto destino, onde o voo será finalizado.

- **Preço Máximo**: é o preço máximo que o usuário quer para a passagem. O sistema somente pegará os voos que forem mais baratos ou tiverem o mesmo preço.

- **E-mail**: o e-mail para onde será enviado a tabela com os voos encontrados

### 2 - Inicialização das Classes de Busca:
- Utilizando as informações inseridas pelo usuário, o sistema inicializa as classes de busca e executa a busca das passagens para cada uma delas.

### 3 - Criação da Tabela:
- Após obter as informações sobre os voos, elas são passadas para uma tabela. A tabela é única, portanto, contém informações consolidadas de todos os voos de todas as empresas aéreas.

- **Composição da tabela**
    - **Empresa**: é a empresa aérea do voo
    - **Partida**: data e horário de partida do voo;
    - **Chegada**: data e horário de chegada do voo;
    - **Conexões**: é o número de conexões que o voo possui;
    - **Preço**: preço da passagem no momento da busca
    - **Link**: é o link para acesssar o voo.

### 4 - Envio da Tabela:
Após a criação da tabela, a mesma é enviada para o e-mail que o usuário informou no início


## Execução
### 1 - Clonagem

### 2 - Entrar no repositório 
### 3 - Executar o arquivo main
### 4 - Inserir os dados
### 5 - Esperar finalização das buscas
### 6 - Verificar o e-mail

## Tecnologias
- Python
- Selenium
