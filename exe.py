from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QMessageBox
from PyQt5 import QtGui, QtWidgets
from gui import *
from login import Ui_Login
from gen_pdf import gen_pdv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import mysql.connector
from mysql.connector import Error
import sys


con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)
if con.is_connected():
    db_info = con.get_server_info()
    print("conectado ao servidor msql versao", db_info)


class Login(QWidget, Ui_Login):
    def __init__(self) -> None:
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.btn_login.clicked.connect(self.open_system)

    def open_system(self):
        usuario = self.user.text()
        senha = self.senha.text()
        consult_user = f"""SELECT user From usuarios"""
        consult_password = f"""SELECT senha From usuarios Where user ='{usuario}'"""
        cursor.execute(consult_user)
        user = cursor.fetchone()
        cursor.execute(consult_password)
        password = cursor.fetchone()

        if usuario == user[0] and senha == password[0]:
            self.w = MainWindow()
            self.close()
            self.w.show()
        else:
            self.show_MessageBox()

    def show_MessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Error")
        msg.setText("Usuario Nao Cadastrado")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

       
        ########################    BOTOES DO SISTEMA   ##################################
        self.btn_novo_cadastro.clicked.connect(self.cadastro_cliente)
        self.btn_salvar_selecao.clicked.connect(self.cadastro_orcamento)
        self.btn_salvar_produto.clicked.connect(self.cadastro_produto)
        self.btn_atualizar_produto.clicked.connect(self.mostrar_produtos)
        self.btn_att_cliente.clicked.connect(self.mostrar_clientes)
        self.btn_limpar_cliente.clicked.connect(self.apagar_clientes)
        self.btn_limpar_produto.clicked.connect(self.show_MessageBox)
        self.btn_imprimir.clicked.connect(gen_pdv)

        ############################   PAGINAS DO SISTEMA   ##############################

        self.btn_PDV.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.PDV))
        self.btn_produtos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Produtos))
        self.btn_caixa.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Caixa))
        self.btn_vendas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Vendas))
        self.btn_cliente.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Clientes))
        self.btn_Usuario.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Usuario))

        ###########################     COMBO_BOX       ####################################
        self.combo_projeto.currentIndexChanged.connect(self.endereco_combo)
        self.combo_modelo.currentIndexChanged.connect(self.index_modelo)

        self.endereco_combo()
        self.mostrar_clientes()
        self.mostrar_produtos()


    def endereco_combo(self):
        projeto = self.combo_projeto.currentIndex()

        if projeto == 0:
            self.portas()

        if projeto == 1:
            self.janelas()

    def index_modelo(self):
        modelo = self.combo_modelo.currentIndex()
        if modelo == 0:
            self.img_projeto.clear()
        elif modelo == 1:
            self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE.png"))
        elif modelo == 2:
            self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 1 FIXO.png"))
        elif modelo == 3:
            self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS.png"))
        elif modelo == 4:
            self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS 2 FIXOS.png"))

    def portas(self):
        self.combo_modelo.clear()
        cursor.execute('SELECT Portas FROM portas')
        dados_lidos = cursor.fetchall()
        #dados_lidos = list.portas
        for p in dados_lidos:
            self.combo_modelo.addItems(p)

    def janelas(self):
        self.combo_modelo.clear()
        cursor.execute('SELECT Janelas FROM janelas')
        dados_lidos = cursor.fetchall()
        for j in dados_lidos:
            self.combo_modelo.addItems(j)

    def fechar_conexao(self):
        if con.is_connected():
                cursor.close()
                con.close()
        print("Conexao ao MySql foi encerrada")

    def cadastro_cliente(self):
        #cod = self.box_cliente.value()
        nome = self.line_cliente.text()
        orcamento = self.line_orcamento.text()
        bairro = self.line_bairro.text()
        cidade = self.line_cidade.text()
        endereco = self.line_endereco.text()
        estado = self.line_estado.text()
        #projeto = self.combo_projeto.text()
        telefone = self.line_telefone.text()
        celular = self.line_celular.text()

        inserir_clientes = f"""insert into clientes
                                 (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
                                 values
                                 ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}')"""




        if con.is_connected():
            cursor = con.cursor(buffered=True)
            cursor.execute(inserir_clientes)

            print(inserir_clientes)
            con.commit()

    def mostrar_clientes(self):
        cursor.execute("SELECT * FROM clientes")
        dados_lidos = cursor.fetchall()
        self.tabela_cliente.clearContents()
        self.tabela_cliente.setRowCount(len(dados_lidos))

        for row, text in enumerate(dados_lidos):
            for column, data in enumerate(text):
                self.tabela_cliente.setItem(row, column,QTableWidgetItem(str(data)))

    def apagar_clientes(self):
        #QMessageBox.about(MainWindow,"Confirmar Acao?","Esta Acao excluira todos os itens deseja confirmar?")
        apagar_clientes = f"""DROP TABLE clientes"""

        criar_clientes = f"""CREATE TABLE IF NOT EXISTS`CLIENTES`(
         `id` INT NOT NULL AUTO_INCREMENT, 
         `cliente` VARCHAR(30),
         `orcamento` INT(4) UNIQUE,
         `bairro` VARCHAR(30),
         `cidade` VARCHAR(30) DEFAULT 'SG',
         `endereco` VARCHAR(50),
         `uf` VARCHAR(2) DEFAULT 'RJ',
         `projeto` INT,
         `telefone` INT(11) UNIQUE,
         `celular` INT(11) UNIQUE,
         PRIMARY KEY(id)
         )DEFAULT CHARSET = utf8mb4;"""
        if con.is_connected():
            cursor.execute(apagar_clientes)
            cursor.execute(criar_clientes)
            print(criar_clientes)
            

    def cadastro_orcamento(self):
        produto = self.box_produto.value()
        quantidade = self.box_quantidade.value()
        altura = self.box_altura.value()
        largura = self.box_largura.value()

        declaracao = f"""insert into orcamento
                            (produto, quantidade, altura, largura)
                            values 
                            ('{produto}', '{quantidade}', ' {altura}', ' {largura})'"""
        print(declaracao)
        con.commit()

    def cadastro_produto(self):
        cod = self.box_codigo_produto.value()
        produto = self.line_produto.text()
        desc = self.line_descricao.text()
        alt = self.box_altura_produto.value()
        lar = self.box_largura_produto.value()
        com = self.box_comprimento_produto.value()
        val = self.box_valor_produto.value()

        inserir_produtos = f"""INSERT INTO produtos
                (id, produto, descricao, altura, largura, valor, comprimento)
                VALUES
                ('{cod}','{produto}','{desc}','{alt}','{lar}','{val}','{com}')"""

        if con.is_connected():
            cursor = con.cursor(buffered=True)
            cursor.execute(inserir_produtos)
            print(inserir_produtos)
            con.commit()

    def mostrar_produtos(self):
        cursor.execute("SELECT * FROM produtos")
        dados_lidos = cursor.fetchall()
        self.tabela_prodtuos.clearContents()
        self.tabela_prodtuos.setRowCount(len(dados_lidos))


        for row, text in enumerate(dados_lidos):
            for column, data in enumerate(text):
                self.tabela_prodtuos.setItem(row, column, QTableWidgetItem(str(data)))

    def show_MessageBox(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS ITENS DA TABELA,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        msg.buttonClicked.connect(self.what_button)
        msg.exec_()

    def what_button(self, dialog_button):
        btn = dialog_button.text()
        if btn == "OK":
            try:
                apagar_produto = f"""DROP TABLE produtos"""

                criar_produto = f"""CREATE TABLE IF NOT EXISTS `produtos` (
                                `id` INT(11) NOT NULL,
                                `produto` VARCHAR(45) NULL,
                                `descricao` VARCHAR(60) NULL,
                                `altura` DECIMAL(4,2) NULL,
                                `largura` DECIMAL(4,2) NULL,
                                `valor` DECIMAL(6,2) NULL,
                                `comprimento` DECIMAL(4,2) NULL,
                                 PRIMARY KEY (id)
                                )DEFAULT CHARACTER SET = utf8mb4;"""
                cursor.execute(apagar_produto)
                cursor.execute(criar_produto)

            except Error:
                print(Error)

            finally:
                print(apagar_produto)
                print(criar_produto)

        else:
            print("Acao Cancelada")




if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    login = Login()
    login.show()
    sys.exit(app.exec_())

