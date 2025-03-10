import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime
import json
from unidecode import unidecode
from functools import partial
import os


class Janela(tk.Tk):

    # ---------- MÉTODOS PRIVADOS ----------
    def _buscar_voos(self):

        # Pegando as infomações que o usuário Inseriu
        outbound = self.calendario_inicio.get()
        inbound = self.calendario_final.get()
        origin = self.selecionar_origem.get()[-3:]
        destination = self.selecionar_destino.get()[-3:]
        precoMaximo = self.entry_preco_maximo.get()
        email = self.entry_email.get()

        # Calculando a diferenca em dias entre o ultimo e primeiro dia do periodo da viagem
        diferenca = str(((datetime.strptime(inbound, "%d-%m-%Y")) - datetime.strptime(outbound, "%d-%m-%Y")).days)
        
        os.environ['OUTBOUND'] = outbound
        os.environ['INBOUND'] = inbound
        os.environ['ORIGIN'] = origin
        os.environ['DESTINATION'] = destination
        os.environ['PRECO_MAXIMO'] = precoMaximo
        os.environ['EMAIL'] = email
        os.environ['DIFERENCA'] = diferenca

        self.destroy()

        
    def _verificando_campos(self, *args):
        self.validacao = 6
        # Verificando se todos os campos foram preenchidos
        # Cada campo já se verifica se foi preenchido corretamente

        # Data inicial e final
        data_inicial = self.calendario_inicio.get()
        data_final = self.calendario_final.get()

        if data_inicial: self.validacao -=1
        if data_final: self.validacao -= 1


        # Origem e destino
        origem = self.selecionar_origem.get()
        destino = self.selecionar_destino.get()

        if origem: self.validacao -= 1
        if destino: self.validacao -= 1

        # Preco maximo
        preco = self.entry_preco_maximo.get()
        if preco: self.validacao -= 1

        # Email
        email = self.entry_email.get()
        if email and "@" in email and ".com" in email: self.validacao -= 1

        if self.validacao == 0:
            self.entry_buscar["state"] = "active"
        else:
            self.entry_buscar["state"] = "disabled"


    def _verificar_origem(self, *args):
        # Origem e destino devem ser diferentes, caso o destino já esteja preenchidos
        origem = self.selecionar_origem.get()
        destino = self.selecionar_destino.get()
        
        if destino:
            if origem == destino:
                self.label_origem["text"] = "Origem e destino devem ser diferentes"
                self.label_origem["fg"] = "red"
                self.selecionar_origem.set("")
            else:
                self.label_origem["text"] = "Cidade de origem"
                self.label_origem["fg"] = "black"     
      
    def _verificar_destino(self, *args):
        # Origem e destino devem ser diferentes, caso o destino já esteja preenchidos
        origem = self.selecionar_origem.get()
        destino = self.selecionar_destino.get()
        
        if origem:
            if origem == destino:
                self.label_destino["text"] = "Origem e destino devem ser diferentes"
                self.label_destino["fg"] = "red"
                self.selecionar_destino.set("")
            else:
                self.label_destino["text"] = "Cidade de destino"
                self.label_destino["fg"] = "black"      


    def _verificar_data_inicial(self, *args):
        # Verificando se a data inicial é posterior ou igual ao dia de hoje
        hoje = datetime.today().strftime("%d-%m-%Y")
        hoje = datetime.strptime(hoje,"%d-%m-%Y")
        data_calendario = self.calendario_inicio.get()
        data_calendario = datetime.strptime(data_calendario, "%d-%m-%Y")

        if hoje > data_calendario:
            self.label_calendario["text"] = "Data inicial deve ser posterior ou igual a data de hoje"
            self.label_calendario["fg"] = "red"
            self.calendario_inicio.set_date(hoje) 
        else:
            self.label_calendario["text"] = "Escolha a data do início do perído que deseja viajar"
            self.label_calendario["fg"] = "black"            

            # Atualizando a data final para a mesma da data inicial
            data = self.calendario_inicio.get_date()
            self.calendario_final.set_date(data)


    def _verificar_data_final(self, *args):
        # Verificando se a data final é posterior ou igual a data inicial
        if self.calendario_inicio.get_date() > self.calendario_final.get_date():
            self.label_calendario2["text"] = "Data final deve ser posterior ou igual a data inicial"
            self.label_calendario2["fg"] = "red"
            self.calendario_final.set_date(self.calendario_inicio.get_date())
        else:
            self.label_calendario2["text"] = "Escolha a data do final do perído que deseja viajar"
            self.label_calendario2["fg"] = "black"


    def _verificar_inicial(self, widget, input):
        input = unidecode(input.upper())
        widget["values"] = [f"{aeroporto[0]} / {aeroporto[1]} - {aeroporto[2]}" for aeroporto in self.aeroportos if aeroporto[0].upper().startswith(input)]
        # widget.event_generate("<Down>")
        # widget.event_generate("<Escape>")

        return True
    

    def _verificar_email(self, input):
        if "@" in input and ".com" in input:
            self.label_email["text"] = "Informe seu e-mail"
            self.label_email["fg"] = "black"
            return True
        else:        
            self.label_email["text"] = "Informe um email válido"
            self.label_email["fg"] = "red"
            return True
            

    def _verificar_preco(self, input):
        if input.isdigit():
            self.label_preco["text"] = "Preço Máximo"
            self.label_preco["fg"] = "black"            
            return True
        elif input == "":
            return True
        else:
            self.label_preco["text"] = "Digite apenas números"
            self.label_preco["fg"] = "red"
            return False


    # --------------------
    def __init__(self, listaAeroportos):
        super().__init__()
        self.title("Buscador De Voos")
        self.validacao = 6
        self.aeroportos = listaAeroportos


        # ---------- TÍTULO DA JANELA ----------
        self.label_titulo = tk.Label(text="Verificação de preços de passagens", bg="black", fg="White")
        self.label_titulo.grid(row=0, column=0, columnspan=3, padx=10, pady=10, sticky="NSEW")
       

        # ---------- PRIMEIRA DATA ----------
        self.label_calendario = tk.Label(text="Escolha a data do início do perído que deseja viajar")
        self.label_calendario.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

        self.calendario_inicio = DateEntry(year=2025, locale="pt_br", date_pattern='dd-mm-yyyy')
        self.calendario_inicio.grid(row=1, column=2, padx=10, pady=10, sticky="NSEW")
        self.calendario_inicio.bind("<<DateEntrySelected>>", self._verificar_data_inicial)
        self.calendario_inicio.bind("<Motion>", self._verificando_campos)

        # ---------- ÚLTIMA DATA ----------
        self.label_calendario2 = tk.Label(text="Escolha a data do final do perído que deseja viajar")
        self.label_calendario2.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="NSEW")

        self.calendario_final = DateEntry(year=2025, locale="pt_br", date_pattern='dd-mm-yyyy')
        self.calendario_final.grid(row=2, column=2, padx=10, pady=10, sticky="NSEW")
        self.calendario_final.bind("<<DateEntrySelected>>", self._verificar_data_final)
        self.calendario_final.bind("<Motion>", self._verificando_campos)

        # ---------- ORIGEM ----------
        aeroportos = [f"{aeroporto[0]} / {aeroporto[1]} - {aeroporto[2]}" for aeroporto in self.aeroportos]

        self.label_origem = tk.Label(text="Cidade de origem")
        self.label_origem.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='NSEW')

        self.selecionar_origem = ttk.Combobox(values=aeroportos, width=40)
        self.selecionar_origem.grid(row=3, column=2, padx=10, pady=10, sticky="NSEW")
        self.selecionar_origem.bind("<<ComboboxSelected>>", self._verificar_origem)
        self.selecionar_origem.bind("<Motion>", self._verificando_campos) 

        # A lista de origem deve ser editada para conter apenas as cidades cuja inicial seja a que o usuário esteja digitando
        # Será passado como parâmetro para a função: self.selecionar_origem e input
        ve_inicial = (self.register(partial(self._verificar_inicial, self.selecionar_origem)), "%P")
        self.selecionar_origem.config(validate="key", validatecommand=ve_inicial)


        # ---------- DESTINO ----------
        self.label_destino = tk.Label(text="Cidade de Destino")
        self.label_destino.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky='NSEW')

        self.selecionar_destino = ttk.Combobox(values=aeroportos, width=40)
        self.selecionar_destino.grid(row=4, column=2, padx=10, pady=10, sticky="NSEW")
        self.selecionar_destino.bind("<<ComboboxSelected>>", self._verificar_destino)
        self.selecionar_destino.bind("<Motion>", self._verificando_campos)  
        ve_inicial = (self.register(partial(self._verificar_inicial, self.selecionar_destino)), "%P")
        self.selecionar_destino.config(validate="key", validatecommand=ve_inicial)


        # ---------- PREÇO MÁXIMO ---------- 
        self.label_preco = tk.Label(text="Preço Máximo")
        self.label_preco.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='NSEW')

        self.entry_preco_maximo = tk.Entry()
        self.entry_preco_maximo.grid(row=5, column=2, padx=10, pady=10, sticky='NSEW')
        self.entry_preco_maximo.config(validate="key", validatecommand=(self.register(self._verificar_preco), '%P'))
        self.entry_preco_maximo.bind("<Motion>", self._verificando_campos)    

        # ---------- EMAIL ---------- 
        self.label_email = tk.Label(self, text="Informe seu e-mail")
        self.label_email.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="NSWE")

        self.entry_email = tk.Entry(width=20)
        self.entry_email.grid(row=6, column=2, padx=10, pady=10, sticky='NSEW')
        vem = (self.register(self._verificar_email), "%P")
        self.entry_email.config(validate="key", validatecommand=vem)
        self.entry_email.bind("<Motion>", self._verificando_campos)    
        try:
            with open("email.txt", "r") as f:
                self.entry_email.insert(0, f.read()) 
        except:
            pass

        # ---------- BOTÃO ----------
        self.entry_buscar = tk.Button(text="Buscar Voos", command=self._buscar_voos, state="disabled")
        self.entry_buscar.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky='NSEW')