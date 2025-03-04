import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, timedelta
from email import encoders
import pandas as pd
import time
import requests
from unidecode import unidecode 

# ------------------------------------ DIFENÇA DE HORARIO ------------------------------------
def fun_diferenca_horario(passagem, classe, data_partida_voo, primeiro, segundo):
    partida_onibus = passagem.find_element(By.CLASS_NAME,classe).text
    partida_onibus = f"{data_partida_voo} {partida_onibus}:00"                
    partida_onibus = datetime.strptime(partida_onibus, "%Y-%m-%d %H:%M:%S")
    return (primeiro - segundo).total_seconds()/3600   


# ------------------------------------ REMOVENDO HORA ------------------------------------
def removendo_hora(valor):
    return valor[:5]


# ------------------------------------ NOME DAS CIDADES DOS AEROPORTOS ------------------------------------
def get_city_from_iata(iata_code):
    api_url = f'https://api.api-ninjas.com/v1/airports?iata={iata_code}'
    response = requests.get(api_url, headers={'X-Api-Key': 'ptMiBhL8QRZnTaFpYO6z7S5eEU6dYnneTTT8BDz1'})

    if response.status_code == requests.codes.ok:
        data = response.json()
        city = data[0].get("city") if data else None
        return city
    else:
        print(f"Error ({response.status_code}): {response.text}")
        return None



# ------------------------------------ ENVIO DE EMAIL ------------------------------------
def enviar_email(destinatario, origin, destination, nome_tabela=None, preco_maximo=None, outbound=None, inbound=None, tem_voo=False, tem_onibus=False):
    msg = MIMEMultipart()

    # -------------------- AVIÃO --------------------
    if tem_onibus==False:
        origin = get_city_from_iata(origin)
        destination =get_city_from_iata(destination)        

        periodo = f"{outbound.replace('-','/')} - {inbound.replace('-','/')}"
        

        if tem_voo:
            corpo_email = f"""
            <html>
                <body>
                    <h2 style="color: #4CAF50;">Passagens encontradas para {periodo}</h2>
                    <p>Origem: {origin}</p>
                    <p>Destino: {destination}</p>
                </body>
            </html>
            """
            msg.attach(MIMEText(corpo_email, 'html'))

            # Anexando a tabela com os voos
            filename = f'{nome_tabela}'
            attachment = open(f'{nome_tabela}', 'rb')

            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
            msg.attach(part)
            attachment.close()
        else:
            corpo_email = f"""
            <html>
                <body>
                    <h2 style="color: #FF5733;">Não foram encontrados voos abaixo de R$ {preco_maximo:.2f} para {periodo}</h2>
                    <p>Origem: {origin}</p>
                    <p>Destino: {destination}</p>
                </body>
            </html>
            """
            msg.attach(MIMEText(corpo_email, 'html'))

    # -------------------- ÔNIBUS --------------------
    if tem_onibus:
        corpo_email = f"""
        <html>
            <body>
                <h2 style="color: #4CAF50;">Passagens de Avião e Ônibus</h2>
                <p>Origem: {origin}</p>
                <p>Destino: {destination}</p>
            </body>
        </html>
        """
        msg.attach(MIMEText(corpo_email, 'html'))

        # Anexando a tabela com os voos
        filename = f'{nome_tabela}'
        attachment = open(f'{nome_tabela}', 'rb')

        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(part)
        attachment.close()

    msg['Subject'] = "PASSAGENS"
    msg['From'] = 'pedrovbittencourt@gmail.com'
    msg['To'] = destinatario
    password = 'speaodkjrwxkqjnb'

    # Enviando o Email
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(msg['From'], password)
    s.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))
    s.quit()



# ------------------------------------ VARIÁVEIS PARA A TABELA ------------------------------------
empresas = []
datas_partidas = []
datas_chegadas = []
conexoes = []
precos = []
links = []



# ------------------------------------ LATAM ------------------------------------
def busca_latam(outbound, origin, destination, intervalo_tempo, preco_maximo,navegador):
    outbound = datetime.strptime(outbound, '%d-%m-%Y').strftime('%Y-%m-%d')

    link = f"https://www.latamairlines.com/br/pt/oferta-voos/?origin={origin}&outbound={outbound}T12%3A00%3A00.000Z&destination={destination}&inbound=null&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"
    navegador.get(link)

    try:
        navegador.find_element(By.ID, "cookies-politics-button").click()
    except:
        pass

    # Alternando entre as datas
    for i in range(intervalo_tempo):
        # Esperando os voos carregarem
        while len(navegador.find_elements(By.CLASS_NAME,'kKMdJR')) < 1:
            time.sleep(1)

        # Lista com todos os voos
        lista_voos = navegador.find_elements(By.CLASS_NAME,'kKMdJR')

        # Verificando o preço de cada voo e pegando o link dos voos 'baratos'
        for voo in lista_voos:
            # Preço do voo
            preco = voo.find_element(By.CLASS_NAME,'koxMWe').text[4:]
            preco = float(preco.replace('.','').replace(',','.'))

            if preco < preco_maximo:
                precos.append(preco)
                
                # ----- DATA -----
                data_partida = navegador.find_element(By.ID,'date-carousel-item-3').text
                data_partida = data_partida[6:].replace("/","-")

                data_partida = f"{outbound[:4]}-{data_partida}"
                data_partida = datetime.strptime(data_partida, "%Y-%d-%m")     

                data_chegada = data_partida
                
                # ----- LINK ----
                link_voo = f"https://www.latamairlines.com/br/pt/oferta-voos/?origin={origin}&outbound={data_partida.strftime('%Y-%m-%d')}T12%3A00%3A00.000Z&destination={destination}&inbound=null&adt=1&chd=0&inf=0&trip=OW&cabin=Economy&redemption=false&sort=RECOMMENDED"
                links.append(link_voo)

                # ----- HORARIO ----- 
                horarios_voos = voo.find_elements(By.CLASS_NAME,'kvztEO')

                # Ajeitando o horario
                for i, horario in enumerate(horarios_voos):
                    horario = horario.text.replace("\n","")

                    # Avião chega no proximo dia
                    if(len(horario)) > 5:
                        horario = horario[:4]
                        data_chegada += timedelta(days=1)

                    # Ajeitando "2:20" para "02:20"
                    if(len(horario)) < 5:
                        horario = f"0{horario}"

                    horarios_voos[i] = horario

                # Pegando os horarios de partida e chegada
                hora_partida = horarios_voos[0]
                hora_chegada = horarios_voos[1]

                # Formatando para string
                data_partida = data_partida.strftime("%d/%m")
                data_chegada = data_chegada.strftime("%d/%m")

                # Juntando a data e hora
                partida = f"{data_partida}  {hora_partida}"
                chegada = f"{data_chegada}  {hora_chegada}"

                datas_partidas.append(partida)
                datas_chegadas.append(chegada)

                # ----- CONEXÕES ----- 
                conexao = voo.find_element(By.CLASS_NAME,'dtpzom').text[:1]
                if conexao == "D": conexao = "Direto"
                conexoes.append(conexao)

                empresas.append("LATAM")
                        
        navegador.find_element(By.ID,'date-carousel-item-4').click()
        time.sleep(3)



# ------------------------------------ GOL ------------------------------------
def busca_gol(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador):
    # Trasformando o dia e mês em data
    data_atual = datetime.strptime(outbound, '%d-%m-%Y')
    
    for i in range(intervalo_tempo):
        outbound = data_atual.strftime('%d-%m-%Y')
        # Entrando nas datas
        navegador.get(f"https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de={origin}&para={destination}&ida={outbound}&ADT=1&CHD=0&INF=0")
        # time.sleep(600)

        # Aceitando os cookies automaticamente
        if i == 1:
            try:
                navegador.find_element(By.ID, "onetrust-accept-btn-handler").click()
            except:
                pass

        # Esperando os voos carregarem
        while len(navegador.find_elements(By.CLASS_NAME,'p-select-flight__accordion')) < 1:
            time.sleep(1)
        time.sleep(1)

        # Pegando uma lista com todos os voo
        voos =  navegador.find_elements(By.CLASS_NAME,'p-select-flight__accordion')
        
        # Pecorrendo todos os voos
        for i, voo in enumerate(voos):
            # Pegando,pelo id, o preço dos voos    
            preco = float(voo.find_element(By.ID,f"lbl_priceValue_{i + 1}_emission").text[2:].replace(".",'').replace(",",'.'))

            # Filtrando os voos de acordo com o preco_maximo
            if preco < preco_maximo:
                # ----- PREÇO -----
                precos.append(preco)

                # ----- LINK -----
                link = f"https://b2c.voegol.com.br/compra/busca-parceiros?pv=br&tipo=DF&de={origin}&para={destination}&ida={outbound}&ADT=1&CHD=0&INF=0"
                links.append(link)

                # ----- DATA -----
                data_partida = data_atual.strftime("%d/%m")
                data_chegada = data_partida

                # Pegando horarios de partida e chegada
                hora_partida = voo.find_element(By.ID, f'lbl_origin_{i + 1}_emission').text[6:]
                hora_chegada = voo.find_element(By.ID, f'lbl_destination_{i + 1}_emission').text[6:]

                # Verificando se o voo chega no proximo dia
                if int(hora_chegada[:2]) < int(hora_partida[:2]):
                    data_chegada = data_atual.strftime("%Y/%d/%m")
                    data_chegada = datetime.strptime(data_chegada, "%Y/%d/%m")
                    data_chegada += timedelta(days=1)
                    data_chegada = data_chegada.strftime("%d/%m")

                # Juntando a data e hora
                partida = f"{data_partida}  {hora_partida}"
                chegada = f"{data_chegada}  {hora_chegada}"

                datas_partidas.append(partida)
                datas_chegadas.append(chegada)
 
                # Conexões
                conexao = voo.find_element(By.ID,f'lbl_segment_{i + 1}_emission').text[:1]
                conexoes.append(conexao)

                empresas.append("GOL")

        # Mudando para o próximo dia
        data_atual += timedelta(days=1)



# ------------------------------------ VIAÇÃO GARCIA ------------------------------------
def buscar_onibus(cidade_ori, estado_ori, cidade_des, estado_des, ano, primeiro, navegador):

    passagens = []

    # CIDADE DE ORIGEM E DESTINO
    origin = f"{unidecode(cidade_ori).lower().replace(' ','-')}-{unidecode(estado_ori).lower()}"
    destination = f"{unidecode(cidade_des).lower().replace(' ','-')}-{unidecode(estado_des).lower()}"

    # LENDO A TABELA
    tabela = pd.read_excel('Voos.xlsx')
    
    # PECORRENDO A TABELA
    for indice, linha in tabela.iterrows():

        # -------------------- DETALHES DO VOO --------------------
        # ---------- PARTIDA VOO ----------
        data_partida_voo = f"{ano}-{linha['Data Partida'][:5]}".replace('/','-')
        data_partida_voo = datetime.strptime(data_partida_voo, "%Y-%d-%m").strftime("%Y-%m-%d")

        # Pegando a hora do voo
        hora_partida_voo = linha['Horario'][:5]

        # Partida do voo
        partida_voo = f"{data_partida_voo} {hora_partida_voo}"
        partida_voo = datetime.strptime(partida_voo, "%Y-%m-%d %H:%M")

        # ---------- CHEGADA VOO ----------
        # Hora de chegada do voo
        hora_chegada_voo = linha['Horario'][8:].replace('/','-') 

        # Data de chegada do voo, antes da verificação do horario
        data_chegada_voo = data_partida_voo

        if linha['Empresa'] == 'LATAM':
            # verficando casos do tipo "1:55 + 1" e modificando a data de chegada do voo
            if len(hora_chegada_voo) >  5:
                hora_chegada_voo = hora_chegada_voo[:4].replace(":","")
                if len(hora_chegada_voo) < 4:
                    hora_chegada_voo = f"0{hora_chegada_voo[:1]}:{hora_chegada_voo[1:]}"
                data_chegada_voo = datetime.strptime(data_partida_voo, "%Y-%m-%d")
                data_chegada_voo += timedelta(days=1)
                data_chegada_voo = data_chegada_voo.strftime("%Y-%m-%d")
        else:
            # Verificando se o voo chega no outro dia (hora da chegada é mais cedo do que a hora de partida)
            if int(hora_chegada_voo[:2]) < int(hora_partida_voo[:2]):
                data_chegada_voo = datetime.strptime(data_partida_voo, "%Y-%m-%d")
                data_chegada_voo += timedelta(days=1)
                data_chegada_voo = data_chegada_voo.strftime("%Y-%m-%d")

        chegada_voo = f"{data_chegada_voo} {hora_chegada_voo}"
        chegada_voo = datetime.strptime(chegada_voo, "%Y-%m-%d %H:%M")

        # ---------- ENTRANDO NO LINK ----------
        link = f"https://passagens.viacaogarcia.com.br/onibus/{origin}/{destination}?departure_at={data_partida_voo}&skip_not_found_redirect=undefined"
        navegador.get(link) 
        time.sleep(2)
        
        # ---------- DETALHES DO ÔNIBUS ----------
        # Filtrando o navegador para o elemento da pagina que contem todas as viagens
        while len(navegador.find_elements(By.CLASS_NAME, 'routes-list')) < 1:
            time.sleep(0.5)
        lista = navegador.find_element(By.CLASS_NAME, 'routes-list')
        
        melhor_passagem = ("00:00",8)
        tem_passagem = 0
        # Lista com as passagens em si
        passagens_onibus = lista.find_elements(By.CLASS_NAME, "route")
        for passagem in passagens_onibus:

            # ---------- VERIFICANDO A DIFERENÇA ----------
            if primeiro=='onibus':
                chegada_onibus = passagem.find_element(By.CLASS_NAME, "arrival-at").text
                chegada_onibus = f"{data_partida_voo} {chegada_onibus}:00"                
                chegada_onibus = datetime.strptime(chegada_onibus, "%Y-%m-%d %H:%M:%S")
                diferenca_horario = (partida_voo - chegada_onibus).total_seconds()/3600                

                if diferenca_horario >= 2:
                    if diferenca_horario < melhor_passagem[1]:
                        chegada_onibus = chegada_onibus.strftime("%H:%M")
                        melhor_passagem = (chegada_onibus, diferenca_horario)
                        tem_passagem = 1
                else:
                    if tem_passagem == 0:
                        melhor_passagem = ("Sem Horário",0)

            elif primeiro=='aviao':
                partida_onibus = passagem.find_element(By.CLASS_NAME,'departure-at').text
                partida_onibus = f"{data_partida_voo} {partida_onibus}:00"                
                partida_onibus = datetime.strptime(partida_onibus, "%Y-%m-%d %H:%M:%S")
                diferenca_horario = (partida_onibus - chegada_voo).total_seconds()/3600

                if diferenca_horario >= 2:
                    if diferenca_horario < melhor_passagem[1]:
                        partida_onibus = partida_onibus.strftime("%H:%M")
                        melhor_passagem = (partida_onibus, diferenca_horario)
                        tem_passagem = 1
                else:
                    if tem_passagem == 0:
                        melhor_passagem = ("Sem Horário",0)                        
                print(f"Chegada do voo: {chegada_voo}\nPartida Ônibus: {partida_onibus}\nDiferença: {diferenca_horario}\n\n")

        passagens.append(melhor_passagem[0])            
        print('\n\n')

    tabela['Chegada do Ônibus'] = passagens
    tabela = tabela.sort_values('Preço')
    tabela.to_excel("Voos e Onibus.xlsx", index=False)
    enviar_email(outbound=None, intervalo_tempo=None, destinatario="pedrovbittencourt@gmail.com", preco_maximo=None, origin=origin, destination=destination, tem_voo=False, tem_onibus=True, nome_tabela="Voos e Onibus.xlsx")
    


# ------------------------------------ JUNTANDO OS VOOS ------------------------------------
def buscar_voos(outbound, inbound, origin, destination, intervalo_tempo, preco_maximo, email, navegador):
    intervalo_tempo += 1
    # busca_gol(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)
    busca_latam(outbound, origin, destination, intervalo_tempo, preco_maximo, navegador)

    # Fazendo tabela excel
    if datas_partidas:
        tabela_voos = pd.DataFrame({'Empresa': empresas,'Partida': datas_partidas, 'Chegada': datas_chegadas, 'Conexoes': conexoes, 'Preço':precos, 'Link':links})
        tabela_voos = tabela_voos.sort_values('Preço')
        tabela_voos.to_excel('Voos.xlsx', index=False)
        enviar_email(outbound=outbound, inbound=inbound, destinatario=email, preco_maximo=preco_maximo, origin=origin, destination=destination, tem_voo=True, nome_tabela="Voos.xlsx")
    
    else:
        enviar_email(outbound=outbound, inbound=inbound, destinatario=email, preco_maximo=preco_maximo, origin=origin, destination=destination, tem_voo=False)
    print('E-mail enviado')

 