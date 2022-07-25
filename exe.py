from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QMessageBox, QFileDialog
from PyQt5 import uic
from gui import *
from login import Ui_Login
from gen_pdf import gen_pdv
import mysql.connector
from mysql.connector import Error
import sys
from datetime import datetime
import os
from connection import Data_base

db = Data_base()

tempo = datetime.now()
data = tempo.strftime("%x")
hora = tempo.strftime("%X")
resumed = data + " " + hora


class Login(QWidget, Ui_Login):
    def __init__(self) -> None:
        super(Login, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Login")
        self.btn_login.clicked.connect(self.check_user)
        self.btn_login.clicked.connect(self.checkLogin)

    def check_user(self):
        user = self.user.text()
        senha = self.senha.text()
        result = db.select_user(user)

        for i in result:
            if i[0].upper() == user.upper() and i[1].upper() == senha.upper() and i[2] == "Administrador":
                return "Admin"
            elif i[0].upper() == user.upper() and i[1].upper() == senha.upper() and i[2] == "Usuario":
                return "User"
            else:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText("Usuario Nao Cadastrado")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()

    def checkLogin(self):
        autenticacao = self.check_user()
        if autenticacao == "Admin" or autenticacao == "User":
            self.w = MainWindow(autenticacao)
            self.w.show()
            self.close()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Error")
            msg.setText("Usuario Nao Cadastrado")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, user):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(1000, 800)

        if user.lower() == "admin":
            self.btn_Usuario.setVisible(True)
        elif user.lower() == "user":
            self.btn_Usuario.setVisible(False)

        ############################   PAGINAS DO SISTEMA   ##############################

        self.btn_PDV.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.PDV))
        self.btn_produtos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Produtos))
        self.btn_caixa.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Caixa))
        self.btn_vendas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Vendas))
        self.btn_cliente.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Clientes))
        self.btn_Usuario.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Usuario))

        # BOTOES SALVAR
        self.btn_novo_cadastro.clicked.connect(self.cadastro_cliente)
        self.btn_salvar_produto.clicked.connect(self.cadastro_produto)
        self.btn_salvar_user.clicked.connect(self.cadastro_usuario)

        # BOTOES ATUALIZAR
        self.btn_atualizar_produto.clicked.connect(self.mostrar_produtos)
        self.btn_att_cliente.clicked.connect(self.mostrar_clientes)

        # BOTOES APAGAR
        self.btn_limpar_cliente.clicked.connect(self.apagar_clientes)
        self.btn_limpar_produto.clicked.connect(self.apagar_produtos)
        self.btn_limpar_user.clicked.connect(self.apagar_usuario)
        self.pushButton.clicked.connect(self.excluir_cliente)

        # BOTOES ALTERAR
        self.btn_alt_cliente.clicked.connect(self.show_alt)

        # IMPRIMIR PDF
        self.btn_imprimir.clicked.connect(gen_pdv)
        # self.btn_add.clicked.connect(self.add_item)

        # COMBO_BOX
        self.box_produto.valueChanged.connect(self.select_produto)
        self.combo_modelo.currentIndexChanged.connect(self.imageUpdate)


        #######################################################
        self.mostrar_clientes()
        self.mostrar_produtos()
        self.select_produto()
        self.path_arquivos()

        self.btn_open_file.clicked.connect(self.openFile)
        self.btn_add.clicked.connect(self.consult_orcamento)
        self.btn_cancelar_cadastro.clicked.connect(self.cancelar_cliente)

    def alt_cliente(self):
        #ideia usando return
        cliente = self.alt_cliente.alt_cliente.text()
        if cliente != "":
            consult = db.select_cliente()
            return consult[0]

    def excluir_cliente(self):

        cliente, okPressed = QtWidgets.QInputDialog.getText(self,"Excluir Cliente", "Digite o Nome Do Cliente")
        if okPressed and cliente != "":
            #cliente = excluir_cliente.excluir_cliente.text()
            try:
                db.excluir_cliente(cliente)
                self.show_messagebox("Cliente Apagado", "Cliente Apagado Com Sucesso")
            except Error as error:
                print(error)
                self.show_messagebox("Error", "Erro Ao excluir Cliente")
        else:
            print("Acao Cancelada")

    def show_alt(self):
        alt_cliente.show()

    def imageUpdate(self):
        imagePath = "C:/Users/PC/PycharmProjects/pythonProject1/GIT_PDV/resized"
        currentItem = str(self.combo_modelo.currentText())
        currentImage = '%s/%s.png' % (imagePath, currentItem)
        self.img_projeto.setPixmap(QtGui.QPixmap(currentImage))

    def path_arquivos(self):
        for _, _, arquivo in os.walk('C:/Users/PC/PycharmProjects/pythonProject1/GIT_PDV/resized'):
            for i in arquivo:
                final = i[:-4]
                lista = [final]
                self.combo_modelo.addItems(lista)

    def openFile(self):
        directory = QtWidgets.QFileDialog.getExistingDirectory()
        for _, _, arquivo in os.walk(directory):
            for items in arquivo:
                final = items[:-4]
                lista = [final]
                print(lista)
                self.combo_modelo.addItems(lista)

    def cadastro_cliente(self):
        # cod = self.box_cliente.value()
        nome = self.line_cliente.text()
        orcamento = self.line_orcamento.text()
        bairro = self.line_bairro.text()
        cidade = self.line_cidade.text()
        endereco = self.line_endereco.text()
        estado = self.line_estado.text()
        # projeto = self.combo_projeto.text()
        telefone = self.line_telefone.text()
        celular = self.line_celular.text()

        try:
            db.insert_cliente(nome, orcamento, bairro, cidade, endereco, estado, telefone, celular, resumed)
        except Error as error:
            print(f"Erro ao inserir Cliente:{error}")
            self.show_messagebox("Error", "Erro Ao Cadastrar Cliente")
        finally:
            self.show_messagebox("Cliente Cadastrado", "Cliente Cadastrado Com Sucesso")

    def mostrar_clientes(self):
        clientes = db.select_cliente()
        self.tabela_cliente.clearContents()
        self.tabela_cliente.setRowCount(len(clientes))

        for row, text in enumerate(clientes):
            for column, data in enumerate(text):
                self.tabela_cliente.setItem(
                    row, column, QTableWidgetItem(str(data)))

    def apagar_clientes(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS ITENS DA TABELA,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        exec = msg.exec_()
        if exec == QtWidgets.QMessageBox.Ok:
            try:
                db.drop_clientes()
                db.create_clientes()
            except Error as error:
                self.show_messagebox("Error", error)
            finally:
                self.show_messagebox("Clientes Apagados", "Clientes Apagados Com Sucesso")
        else:
            print("Acao Cancelada")

    def consult_orcamento(self):
        produto = self.box_produto.value()
        quantidade = self.box_quantidade.value()
        altura = self.box_altura.value()
        largura = self.box_largura.value()

        db.select_valor(produto)

    def cadastro_produto(self):

        cod = self.box_codigo_produto.value()
        produto = self.line_produto.text()
        desc = self.line_descricao.text()
        alt = self.box_altura_produto.value()
        lar = self.box_largura_produto.value()
        com = self.box_comprimento_produto.value()
        val = self.box_valor_produto.value()
        try:
            db.insert_produto(cod, produto, desc, alt, lar, val, com)
        except Error as error:
            self.show_messagebox("Erro", error)
        finally:
            self.show_messagebox("Concluido", "Produto Cadastrado Com Sucesso")

    def mostrar_produtos(self):
        produtos = db.select_all_produto()

        self.tabela_prodtuos.clearContents()
        self.tabela_prodtuos.setRowCount(len(produtos))

        for row, text in enumerate(produtos):
            for column, data in enumerate(text):
                self.tabela_prodtuos.setItem(
                    row, column, QTableWidgetItem(str(data)))

    def apagar_produtos(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS ITENS DA TABELA,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        exec = msg.exec_()

        if exec == QtWidgets.QMessageBox.Ok:
            try:
                db.drop_produto()
                db.create_produto()
            except Error as error:
                self.show_messagebox("Error", error)
            finally:
                self.show_messagebox("Concluido", "Produtos Apagados Com Sucesso")

        else:
            print("Acao Cancelada")

    def select_produto(self):
        cod = self.box_produto.value()
        try:
            produto = db.select_produto(cod)
            if produto == "":
                for i in produto:
                    self.combo_produto.clear()
                    self.combo_produto.addItem("PRODUTO INDEFINIDO")
            else:
                for i in produto:
                    self.combo_produto.clear()
                    self.combo_produto.addItem(i)
        except Error as error:
            self.show_messagebox("Error", error)

    def apagar_usuario(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS USUARIOS,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        exec = msg.exec_()

        if exec == QtWidgets.QMessageBox.Ok:

            try:
                db.drop_user()
                db.create_user()
            except Error as error:
                self.show_messagebox("Error", error)

            finally:
                self.show_messagebox("Concluido", "Usuarios Apagados com Sucesso")
        else:
            print("Acao Cancelada")

    def cadastro_usuario(self):
        nome = self.lineEdit_6.text()
        email = self.lineEdit_8.text()
        user = self.lineEdit_5.text()
        senha = self.lineEdit_4.text()
        perfil = self.combo_perfil_user_2.currentText()

        try:
            db.insert_user(nome, email, user, senha, perfil)
            self.show_messagebox("Sucesso", "Usuario Cadastrado Com Sucesso")

        except Error as error:
            print(error)
            self.show_messagebox("Error", "Erro Ao Cadastrar Usuario")

    def cancelar_cliente(self):
        self.box_cliente.clear()
        self.line_cliente.clear()
        self.line_bairro.clear()
        self.line_cidade.clear()
        self.line_celular.clear()
        self.line_telefone.clear()
        self.line_estado.clear()
        self.line_endereco.clear()
        self.line_orcamento.clear()

    def show_messagebox(self, title, text):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle(title)
        msg.setText(str(text))
        msg.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    alt_cliente = uic.loadUi("alterar_clientes.ui")
    excluir_cliente = uic.loadUi("excluir_clientes.ui")
    inserir_cliente = uic.loadUi("inserir_clientes.ui")
    login = Login()
    login.show()
    # w = MainWindow()
    # w.show()
    sys.exit(app.exec_())
