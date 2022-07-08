import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os.path
import pickle

class Estudante:

    def __init__(self, nroMatric, nome):
        self.__nroMatric = nroMatric
        self.__nome = nome

    def getNroMatric(self):
        return self.__nroMatric
    
    def getNome(self):
        return self.__nome

class LimiteInsereEstudantes(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title("Estudante")
        self.controle = controle

        self.frameNro = tk.Frame(self)
        self.frameNome = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameNro.pack()
        self.frameNome.pack()
        self.frameButton.pack()
      
        self.labelNro = tk.Label(self.frameNro,text="Nro Matrícula: ")
        self.labelNome = tk.Label(self.frameNome,text="Nome: ")
        self.labelNro.pack(side="left")
        self.labelNome.pack(side="left")  

        self.inputNro = tk.Entry(self.frameNro, width=20)
        self.inputNro.pack(side="left")
        self.inputNome = tk.Entry(self.frameNome, width=20)
        self.inputNome.pack(side="left")             
      
        self.buttonSubmit = tk.Button(self.frameButton ,text="Enter")      
        self.buttonSubmit.pack(side="left")
        self.buttonSubmit.bind("<Button>", controle.enterHandler)
      
        self.buttonClear = tk.Button(self.frameButton ,text="Clear")      
        self.buttonClear.pack(side="left")
        self.buttonClear.bind("<Button>", controle.clearHandler)  

        self.buttonFecha = tk.Button(self.frameButton ,text="Concluído")      
        self.buttonFecha.pack(side="left")
        self.buttonFecha.bind("<Button>", controle.fechaHandler)


    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

class LimiteMostraEstudantes():
    def __init__(self, str):
        messagebox.showinfo('Lista de alunos', str)
        
class LimiteConsultaEstudantes():
    def __init__(self,controle, janela):
        self.controle = controle
        self.janela = janela
        self.my_i = simpledialog.askstring("Consulta","Digite o número de matricula",parent=self.janela)
        self.controle.searchHandler(self.my_i, self )

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

class CtrlEstudante():       
    def __init__(self):
        if not os.path.isfile("estudante.pickle"):
            self.listaEstudantes =  []
        else:
            with open("estudante.pickle", "rb") as f:
                self.listaEstudantes = pickle.load(f)

    def salvaEstudantes(self):
        if len(self.listaEstudantes) != 0:
            with open("estudante.pickle","wb") as f:
                pickle.dump(self.listaEstudantes, f)

    def getEstudante(self, nroMatric):
        estRet = None
        for est in self.listaEstudantes:
            if est.getNroMatric() == nroMatric:
                estRet = est
        return estRet

    def getListaNroMatric(self):
        listaNro = []
        for est in self.listaEstudantes:
            listaNro.append(est.getNroMatric())
        return listaNro

    def insereEstudantes(self):
        self.limiteIns = LimiteInsereEstudantes(self) 
        
    def mostraEstudantes(self):
        str = 'Nro Matric. -- Nome\n'
        for est in self.listaEstudantes:
            str += est.getNroMatric() + ' -- ' + est.getNome() + '\n'       
        self.limiteLista = LimiteMostraEstudantes(str)
    
    def consultaEstudantes(self, janela):
        self.jan = janela
        LimiteConsultaEstudantes(self, self.jan ) 

    def enterHandler(self, event):
        nroMatric = self.limiteIns.inputNro.get()
        nome = self.limiteIns.inputNome.get()
        estudante = Estudante(nroMatric, nome)
        self.listaEstudantes.append(estudante)
        self.limiteIns.mostraJanela('Sucesso', 'Estudante cadastrado com sucesso')
        self.clearHandler(event)

    def clearHandler(self, event):
        self.limiteIns.inputNro.delete(0, len(self.limiteIns.inputNro.get()))
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))

    def searchHandler(self, nr,limite):
        self.limiteCon = limite
        tem = False
        if nr == None:
            self.limiteCon.mostraJanela('Fracasso',"Saindo")  
        else: 
            if nr == "":
                self.limiteCon.mostraJanela('Fracasso',"Digite um número de matriculawb")   
                LimiteConsultaEstudantes(self, self.jan )
            else:
                for a in self.listaEstudantes :    
                    if a.getNroMatric() == nr:
                        tem = True
                        break
                if tem== True:
                    self.limiteCon.mostraJanela('Sucesso ',"Estudante encontrado:"+"\n"+ a.getNome()+ '-'+ a.getNroMatric() + '\n') 
                else:
                    self.limiteCon.mostraJanela('Fracasso',"Estudante não encontrado")
                    LimiteConsultaEstudantes(self, self.jan )
        

    def fechaHandler(self, event):
        self.limiteIns.destroy()
    