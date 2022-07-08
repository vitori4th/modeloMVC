import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import os.path
import pickle

class Disciplina:

    def __init__(self, codigo, nome):
        self.__codigo = codigo
        self.__nome = nome

    def getCodigo(self):
        return self.__codigo
    
    def getNome(self):
        return self.__nome

class LimiteInsereDisciplinas(tk.Toplevel):
    def __init__(self, controle):

        tk.Toplevel.__init__(self)
        self.geometry('250x100')
        self.title("Disciplina")
        self.controle = controle

        self.frameNome = tk.Frame(self)
        self.frameCodigo = tk.Frame(self)
        self.frameButton = tk.Frame(self)
        self.frameCodigo.pack()
        self.frameNome.pack()
        self.frameButton.pack()
      
        self.labelCodigo = tk.Label(self.frameCodigo,text="Código: ")
        self.labelNome = tk.Label(self.frameNome,text="Nome: ")
        self.labelCodigo.pack(side="left")
        self.labelNome.pack(side="left")  

        self.inputCodigo = tk.Entry(self.frameCodigo, width=20)
        self.inputCodigo.pack(side="left")
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

        self.lift 
    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

class LimiteMostraDisciplinas():
    def __init__(self, str):
        messagebox.showinfo('Lista de disciplinas', str)

class LimiteConsultaDisciplinas():
    def __init__(self,controle, janela):
        self.controle = controle
        self.janela = janela
        self.my_i = simpledialog.askstring("Consulta","Digite o número de matricula",parent=self.janela)
        self.controle.searchHandler(self.my_i, self )

    def mostraJanela(self, titulo, msg):
        messagebox.showinfo(titulo, msg)

class CtrlDisciplina():       
    def __init__(self):
        if not os.path.isfile("disciplina.pickle"):
            self.listaDisciplinas =  []
        else:
            with open("disciplina.pickle", "rb") as f:
                self.listaDisciplinas = pickle.load(f)
                
    def salvaDisciplinas(self):
        if len(self.listaDisciplinas) != 0:
            with open("disciplina.pickle","wb") as f:
                pickle.dump(self.listaDisciplinas, f)

    def getListaDisciplinas(self):
        return self.listaDisciplinas

    def getDisciplina(self, codDisc):
        discRet = None
        for disc in self.listaDisciplinas:
            if disc.getCodigo() == codDisc:
                discRet = disc
        return discRet

    def getListaCodDisciplinas(self):
        listaCod = []
        for disc in self.listaDisciplinas:
            listaCod.append(disc.getCodigo())
        return listaCod

    def insereDisciplinas(self):
        self.limiteIns = LimiteInsereDisciplinas(self) 

    def mostraDisciplinas(self):
        str = 'Código -- Nome\n'
        for disc in self.listaDisciplinas:
            str += disc.getCodigo() + ' -- ' + disc.getNome() + '\n'
        self.limiteLista = LimiteMostraDisciplinas(str)

    def consultaDisciplinas(self, janela):
        self.jan = janela
        LimiteConsultaDisciplinas(self, self.jan ) 

    def enterHandler(self, event):
        nroMatric = self.limiteIns.inputCodigo.get()
        nome = self.limiteIns.inputNome.get()
        disciplina = Disciplina(nroMatric, nome)
        self.listaDisciplinas.append(disciplina)
        self.limiteIns.mostraJanela('Sucesso', 'Disciplina cadastrada com sucesso')
        self.clearHandler(event)
    
    def searchHandler(self, nr,limite):
        self.limiteCon = limite
        tem = False

        if nr == None:
            self.limiteCon.mostraJanela('Fracasso',"Saindo")  
        else: 
            if nr == "":
                self.limiteCon.mostraJanela('Fracasso',"Digite um código")   
                LimiteConsultaDisciplinas(self, self.jan )
            else:
                for a in self.listaDisciplinas :    
                    if a.getCodigo() == nr:
                        tem = True
                        break
                if tem== True:
                    self.limiteCon.mostraJanela('Sucesso ',"  Disciplina encontrada:"+"\n"+ a.getNome()+ '-'+ a.getCodigo() + '\n') 
                else:
                    self.limiteCon.mostraJanela('Fracasso',"Disciplina não encontrada")  
                    LimiteConsultaDisciplinas(self, self.jan ) 
                    
    def clearHandler(self, event):
        self.limiteIns.inputCodigo.delete(0, len(self.limiteIns.inputCodigo.get()))
        self.limiteIns.inputNome.delete(0, len(self.limiteIns.inputNome.get()))

    def fechaHandler(self, event):
        self.limiteIns.destroy()
    