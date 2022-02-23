import sys
from datetime import datetime
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.uic import loadUi
import sqlite3



class Token:
    def __init__(self, nome="", email="", entrada=0, saida=0, nvl_Cargo=0):
        self.nome = nome
        self.email = email
        self.nvl_Cargo = nvl_Cargo
        self.entrada = entrada
        self.saida = saida

class User:
    def __init__(self,nome,email,senha,cpf,nvl_Cargo=0,horas_trabalhadas=0):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.cpf = cpf
        self.nvl_Cargo = nvl_Cargo
        self.horas_trabalhadas = horas_trabalhadas


class Tarefa:
    def __init__(self,funcionario,descricao,prazo,prioridade):
        self.funcionario = funcionario
        self.descricao = descricao
        self.prazo = prazo
        self.prioridade = prioridade




class Login(QMainWindow):
    
    def __init__(self):
        super(Login,self).__init__()
        loadUi("tela_login.ui",self)
        self.botao_Login.clicked.connect(self.funcao_login)
        self.botao_CriarConta.clicked.connect(self.funcao_IrTelaCadastro)
        self.linha_Senha.setEchoMode(QtWidgets.QLineEdit.Password)
    
    def funcao_IrTelaCadastro(self):
        criar_Funcionario = telaCadastro()
        widget.addWidget(criar_Funcionario)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def funcao_IrTelaFuncionario(self):
        tela_inicial = telaGerente()
        widget.addWidget(tela_inicial)
        widget.setCurrentIndex(widget.currentIndex()+1)
   
    def gera_token(self):
        token = Token()
        return token 

    def funcao_login(self):
        global user_token
        email = self.linha_User.text()
        senha = self.linha_Senha.text()
        conn = sqlite3.connect('sistemaCompII.db')
        cursor = conn.cursor()
        usuario = cursor.execute(f"""select * from Usuario where email = '{email}'""").fetchone()
        try:
            if(senha == (usuario[2])):
                user_token = self.gera_token()
                user_token.nome = usuario[0]
                user_token.email = usuario[1]
                user_token.nvl_Cargo = usuario[4]
                self.IrTelaInicial()
        except Exception as e:
            print(f"Usuário ou senha inválido")



    def IrTelaInicial(self):
        if user_token.nvl_Cargo == 1:
            tela_inicial = telaFuncionario()
        if user_token.nvl_Cargo == 2:
            tela_inicial = telaGerente()
        widget.addWidget(tela_inicial)
        widget.setCurrentIndex(widget.currentIndex()+1)

    


class telaCadastro(QMainWindow):
    def __init__(self):
        super(telaCadastro,self).__init__()
        loadUi("tela_cadastro.ui",self)
        self.botao_Cadastro.clicked.connect(self.funcao_cadastro)
        self.linha_Senha.setEchoMode(QtWidgets.QLineEdit.Password)
        self.linha_ConfirmaSenha.setEchoMode(QtWidgets.QLineEdit.Password)



    def funcao_cadastro(self):
        nome = self.linha_Nome.text()
        email = self.linha_Email.text()
        cpf = self.linha_CPF.text()
        nvCargo = self.linha_nvlCargo.text()
        senha = self.linha_Senha.text()
        confirma = self.linha_ConfirmaSenha.text()
        try:
            if senha == confirma:
                cadastro = User(nome,email,senha,cpf,nvCargo,0)
                conn = sqlite3.connect('sistemaCompII.db')
                cursor = conn.cursor()
                cursor.execute(f"""insert into Usuario values('{cadastro.nome}','{cadastro.email}','{cadastro.senha}','{cadastro.cpf}','{cadastro.nvl_Cargo}','{cadastro.horas_trabalhadas}')""")
                conn.commit()
                conn.close()
                print("Usuario cadastrado com sucesso!")
        except Exception as e:
            print(f"Ops, algo deu errado com seu\n{e}")
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex()+1)
        



class telaContato(QMainWindow):
    def __init__(self):
        super(telaContato,self).__init__()
        loadUi("tela_contato.ui",self)
        self.botao_EnviarEmail.clicked.connect(self.funcao_contato)    
    
    def funcao_contato(self):
        destinatario = self.linha_Email.text()
        mensagem = self.linha_Texto.text()
        print(f'---------------------\n Destinatário: {destinatario}\n{mensagem}')
        tela_inicio = telaFuncionario()
        widget.addWidget(tela_inicio)
        widget.setCurrentIndex(widget.currentIndex()+1)


class telaTarefa(QMainWindow):
    def __init__(self):
        super(telaTarefa,self).__init__()
        loadUi("tela_novatarefa.ui",self)
        self.botao_Adicionar.clicked.connect(self.adicionaTarefa)
    
    def adicionaTarefa(self):
        funcionario = self.linha_NomeFuncionario.text()
        descricao = self.linha_DescricaoTarefa.text()
        prazo = self.linha_Prazo.text()
        prioridade = self.linha_NivelPrioridade.text()
        try:
            tarefa = Tarefa(funcionario,descricao,prazo,prioridade)
            conn = sqlite3.connect('sistemaCompII.db')
            cursor = conn.cursor()
            cursor.execute(f"""insert into Tarefa values('{tarefa.funcionario}' ,'{tarefa.descricao}','{tarefa.prazo}','{tarefa.prioridade}') """)
            conn.commit()
            conn.close()
            tela_inicial = telaGerente()
            widget.addWidget(tela_inicial)
            widget.setCurrentIndex(widget.currentIndex()+1)
        except Exception as e:
            print(f"{e}")

class telaFuncionario(QMainWindow):
    def __init__(self):
        super(telaFuncionario, self).__init__()
        loadUi("tela_funcionario.ui",self)
        self.tabela_TarefaFuncionario.setColumnWidth(0,100)
        self.tabela_TarefaFuncionario.setColumnWidth(1,100)
        self.tabela_TarefaFuncionario.setColumnWidth(2,100)
        self.botao_Entrada.clicked.connect(self.PontoEntrada)
        self.botao_Saida.clicked.connect(self.PontoSaida)
        self.botao_Att.clicked.connect(self.Atualizar)
        self.botao_Contato.clicked.connect(self.IrContato)
        self.Label_User.setText(f"Olá {user_token.nome},\nHoje é dia {datetime.today().day}/0{datetime.today().month}") 
        self.load_data()


    def load_data(self):
        conn = sqlite3.connect('sistemaCompII.db')
        cursor = conn.cursor()
        query = cursor.execute(f""" select * from Tarefa where funcionario = '{user_token.nome}'    """)
        self.tabela_TarefaFuncionario.setRowCount(20)
        tablerow = 0
        for row in query:
            self.tabela_TarefaFuncionario.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
            self.tabela_TarefaFuncionario.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tabela_TarefaFuncionario.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            self.tabela_TarefaFuncionario.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            tablerow+=1

    def PontoEntrada(self):
        entrada = datetime(datetime.today().year,datetime.today().month,datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
        print(entrada)
        user_token.entrada = entrada
        

    def PontoSaida(self):
        saida = datetime(datetime.today().year,datetime.today().month,datetime.today().day,datetime.today().hour,datetime.today().minute,datetime.today().second)
        print(saida)
        user_token.saida = saida
        tempo_total = user_token.saida - user_token.entrada
        print(f"O tempo total ativo foi de {tempo_total}")

    def Atualizar(self):
        pass

    def IrContato(self):
        contato = telaContato()
        widget.addWidget(contato)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


class telaGerente(QMainWindow):
    def __init__(self):
        super(telaGerente,self).__init__()
        loadUi("tela_gerente.ui",self)
        self.label_User.setText(f"Olá {user_token.nome}, hoje é dia {datetime.today().day}/{datetime.today().month}")
        self.botao_AdicionarTarefa.clicked.connect(self.IrAdicionarTarefa)
        self.botao_Relatorio.clicked.connect(self.funcaoRelatorio)
        self.botao_Contato.clicked.connect(self.IrContato)
        self.botao_Cadastro.clicked.connect(self.IrCadastro)
        self.load_data()

    def load_data(self):
        conn = sqlite3.connect('sistemaCompII.db')
        cursor = conn.cursor()
        query = cursor.execute(f""" select * from Tarefa  group by funcionario""")
        self.tabela_TarefaGerente.setRowCount(20)
        tablerow = 0
        for row in query:
            self.tabela_TarefaGerente.setItem(tablerow,0,QtWidgets.QTableWidgetItem(row[0]))
            self.tabela_TarefaGerente.setItem(tablerow,1,QtWidgets.QTableWidgetItem(row[1]))
            self.tabela_TarefaGerente.setItem(tablerow,2,QtWidgets.QTableWidgetItem(row[2]))
            self.tabela_TarefaGerente.setItem(tablerow,3,QtWidgets.QTableWidgetItem(str(row[3])))
            tablerow+=1

    def IrAdicionarTarefa(self):
        tela_tarefa = telaTarefa()
        widget.addWidget(tela_tarefa)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def IrCadastro(self):
        cadastro = telaCadastro()
        widget.addWidget(cadastro)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def IrContato(self):
        contato = telaContato()
        widget.addWidget(contato)
        widget.setCurrentIndex(widget.currentIndex()+1)


    def funcaoRelatorio(self):
        print("Relatorio realizado com sucesso!")
    
    



App = QApplication(sys.argv)
mainwindown = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindown)
widget.show()
App.exec_()