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

tempo = datetime.now()

data = tempo.strftime("%x")

hora = tempo.strftime("%X")

resumed = data + " " + hora

con = mysql.connector.connect(
    host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)

if con.is_connected():
    db_info = con.get_server_info()
    print("conectado ao servidor msql versao", db_info)


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

        all = f"""SELECT user, senha, perfil FROM usuarios WHERE user='{user}'"""
        cursor.execute(all)
        result = cursor.fetchall()

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

        self.btn_PDV.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.PDV))
        self.btn_produtos.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.Produtos))
        self.btn_caixa.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.Caixa))
        self.btn_vendas.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.Vendas))
        self.btn_cliente.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.Clientes))
        self.btn_Usuario.clicked.connect(
            lambda: self.stackedWidget.setCurrentWidget(self.Usuario))

        ########################    BOTOES SALVAR   ###############################
        self.btn_novo_cadastro.clicked.connect(self.cadastro_cliente)
        # self.btn_salvar_selecao.clicked.connect(self.cadastro_orcamento)
        self.btn_salvar_produto.clicked.connect(self.cadastro_produto)
        self.btn_salvar_user.clicked.connect(self.cadastro_usuario)
        ########################    BOTOES ATUALIZAR    ############################
        self.btn_atualizar_produto.clicked.connect(self.mostrar_produtos)
        self.btn_att_cliente.clicked.connect(self.mostrar_clientes)
        ######################      BOTOES APAGAR       ############################
        self.btn_limpar_cliente.clicked.connect(self.apagar_clientes)
        self.btn_limpar_produto.clicked.connect(self.apagar_produtos)

        ######################      BOTOES ALTERAR      #############################
        self.btn_alt_cliente.clicked.connect(self.show_alt)

        # self.btn_limpar_user.clicked.connect(self.confirmar)
        ######################      IMPRIMIR PDF         ############################
        self.btn_imprimir.clicked.connect(gen_pdv)
        # self.btn_add.clicked.connect(self.add_item)

        self.btn_cancelar_cadastro.clicked.connect(self.cancelar_cliente)

        ###########################     COMBO_BOX       ####################################
        self.box_produto.valueChanged.connect(self.select_produto)
        self.combo_modelo.currentIndexChanged.connect(self.imageUpdate)

        # self.endereco_combo()
        self.mostrar_clientes()
        self.mostrar_produtos()
        self.select_produto()
        self.path_arquivos()
        # self.add_item()

        self.btn_limpar_user.clicked.connect(self.apagar_usuario)
        self.btn_open_file.clicked.connect(self.openFile)
        self.btn_add.clicked.connect(self.consult_orcamento)

    # def endereco_combo(self):
    #     projeto = self.combo_projeto.currentIndex()
    #
    #     if projeto == 0:
    #         self.portas()
    #
    #     if projeto == 1:
    #         self.janelas()

    # def index_modelo(self):
    #     modelo = self.combo_modelo.currentIndex()
    #     if modelo == 0:
    #         self.img_projeto.clear()
    #     elif modelo == 1:
    #         self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE.png"))
    #     elif modelo == 2:
    #         self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 1 FIXO.png"))
    #     elif modelo == 3:
    #         self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS.png"))
    #     elif modelo == 4:
    #         self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS 2 FIXOS.png"))
    #
    # def portas(self):
    #     self.combo_modelo.clear()
    #     cursor.execute('SELECT Portas FROM portas')
    #     dados_lidos = cursor.fetchall()
    #     for p in dados_lidos:
    #         self.combo_modelo.addItems(p)
    #
    # def janelas(self):
    #     self.combo_modelo.clear()
    #     cursor.execute('SELECT Janelas FROM janelas')
    #     dados_lidos = cursor.fetchall()
    #     for j in dados_lidos:
    #         self.combo_modelo.addItems(j)

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

    def fechar_conexao(self):
        if con.is_connected():
            cursor.close()
            con.close()
        print("Conexao ao MySql foi encerrada")

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

        inserir_clientes = f"""insert into clientes
                                 (cliente, orcamento, bairro, cidade, endereço, uf, telefone, celular, data)
                                 values
                                 ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}', '{resumed}')"""

        con = mysql.connector.connect(
            host="localhost", database="jc_vidros", user="root", password="")
        cursor = con.cursor(buffered=True)

        if con.is_connected():
            try:
                cursor.execute(inserir_clientes)
                con.commit()
            except Error as error:
                print(f"Erro ao inserir Cliente:{error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText("Erro Ao Inserir Cliente")
                msg.exec_()
            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Cliente Cadastrado")
                msg.setText("Cliente Cadastrado Com Sucesso")
                msg.exec_()

    def mostrar_clientes(self):
        con = mysql.connector.connect(
            host="localhost", database="jc_vidros", user="root", password="")
        cursor = con.cursor(buffered=True)

        if con.is_connected():
            try:
                cursor.execute("SELECT * FROM clientes")
                dados_lidos = cursor.fetchall()
                self.tabela_cliente.clearContents()
                self.tabela_cliente.setRowCount(len(dados_lidos))

                for row, text in enumerate(dados_lidos):
                    for column, data in enumerate(text):
                        self.tabela_cliente.setItem(
                            row, column, QTableWidgetItem(str(data)))
            except Error as error:
                print(f"Erro ao mostrar cliente: {error}")

    def apagar_clientes(self):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS ITENS DA TABELA,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        exec = msg.exec_()
        if exec == QtWidgets.QMessageBox.Ok:
            apagar_clientes = f"""DROP TABLE clientes"""
            criar_clientes = f"""CREATE TABLE `jc_vidros`.`clientes` (
                                `id` INT NOT NULL AUTO_INCREMENT,
                                `cliente` VARCHAR(45) NULL,
                                `orcamento` VARCHAR(10) NULL,
                                `bairro` VARCHAR(45) NULL,
                                `cidade` VARCHAR(45) NULL DEFAULT 'SG',
                                `endereço` VARCHAR(60) NULL,
                                `uf` VARCHAR(20) NULL,
                                `projeto` VARCHAR(45) NULL DEFAULT 'RJ',
                                `telefone` VARCHAR(20) NULL,
                                `celular` VARCHAR(20) NULL,
                                PRIMARY KEY (`id`),
                                UNIQUE INDEX `telefone_UNIQUE` (`telefone` ASC),
                                UNIQUE INDEX `celular_UNIQUE` (`celular` ASC))
                                ENGINE = InnoDB
                                DEFAULT CHARACTER SET = utf8mb4;"""

            try:
                cursor.execute(apagar_clientes)
                cursor.execute(criar_clientes)
                con.commit()
            except Error as error:
                print(f"Erro Ao Apagar Clientes: {error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"Erro Ao Apagar Clientes {error}")
                msg.setInformativeText("")
                msg.exec_()

            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Clientes Apagados")
                msg.setText("Cliente Apagados Com Sucesso")
                msg.setInformativeText("TODOS OS CLIENTES FORAM APAGADOS")
                msg.exec_()
        else:
            print("Acao Cancelada")

    def consult_orcamento(self):
        produto = self.box_produto.value()
        quantidade = self.box_quantidade.value()
        altura = self.box_altura.value()
        largura = self.box_largura.value()

        consult = f"""SELECT valor FROM produtos WHERE ID= '{produto}'"""

        m2 = altura * largura

        cursor.execute(consult)
        result = cursor.fetchone()
        print(result[0])
        print(m2)

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

        cursor = con.cursor(buffered=True)

        if con.is_connected():
            try:
                cursor.execute(inserir_produtos)
            except Error as error:
                print(f"Erro ao Inserir Produto: {error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Error")
                msg.setText(f"""Error Ao Inserir Produtos
                                {error}""")
                msg.exec_()
            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Produto Cadastrado")
                msg.setText("Produto Cadastrado Com Sucesso")
                msg.exec_()

    def mostrar_produtos(self):
        cursor.execute("SELECT * FROM produtos")
        dados_lidos = cursor.fetchall()
        self.tabela_prodtuos.clearContents()
        self.tabela_prodtuos.setRowCount(len(dados_lidos))

        for row, text in enumerate(dados_lidos):
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
            try:
                cursor.execute(apagar_produto)
                cursor.execute(criar_produto)
                con.commit()

            except Error as error:
                print(f"Erro ao apagar produtos:{error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"""Erro Ao Apagar Produtos
                            {error}""")
                msg.exec_()

            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Produtos Apagados")
                msg.setText("Produtos Apagados Com Sucesso")
                msg.exec_()

        else:
            print("Acao Cancelada")

    def select_produto(self):
        #produto = self.combo_produto

        cod = self.box_produto.value()

        consult = f"""SELECT produto FROM produtos WHERE ID ={cod}"""
        #val = f"""SELECT valor FROM produtos WHERE ID = '{cod}'"""

        if con.is_connected():
            cursor.execute(consult)
            produto = cursor.fetchone()
            # cursor.execute(val)
            #valor = cursor.fetchone()

            if produto == "":
                for i in produto:
                    self.combo_produto.clear()
                    self.combo_produto.addItem("PRODUTO INDEFINIDO")
            else:
                for i in produto:
                    self.combo_produto.clear()
                    self.combo_produto.addItem(i)


# list.append(i)

            # if produto == None:
            #     result = "PRODUTO INDEFINIDO"
            #     for i in result:
            #         self.combo_produto.clear()
            #         self.line_Valor_unit.clear()
            #         self.combo_produto.addItems(result)
            # else:
            #     for i in produto:
            #         self.combo_produto.clear()
            #         self.combo_produto.addItems(i[0])
            #     for f in valor:
            #         self.line_Valor_unit.clear()
            #         self.line_Valor_unit.setText(f[0])

    # def add_item(self):
    #     cod = self.box_produto.value()
    #     projeto = self.combo_produto.currentText()
    #     qt = self.box_quantidade.value()
    #     alt = self.box_altura.value()
    #     lar = self.box_largura.value()
    #
    #     dados = [cod, projeto, qt, alt, lar]
    #
    #     self.tabela_selecao_itens.clearContents()
    #     self.tabela_selecao_itens.setRowCount(len(dados))
    #
    #     for row, text in enumerate(dados):
    #         for collum, data in text:
    #             self.tabela_selecao_itens.setItem(row, collum, QTableWidgetItem(data))

    # print(dados)


    def apagar_usuario(self):
        apagar_usuarios = f"""DROP TABLE IF EXISTS usuarios"""

        criar_usuarios = f"""CREATE TABLE `jc_vidros`.`usuarios` (
                                  `nome` VARCHAR(45) NOT NULL,
                                  `email` VARCHAR(45) NULL,
                                  `user` VARCHAR(45) NULL,
                                  `senha` VARCHAR(45) NULL,
                                  `perfil` VARCHAR(45),
                                  PRIMARY KEY (`nome`),
                                  UNIQUE INDEX `email_UNIQUE` (`email` ASC),
                                  UNIQUE INDEX `user_UNIQUE` (`user` ASC),
                                  UNIQUE INDEX `senha_UNIQUE` (`senha` ASC))
                                ENGINE = InnoDB
                                DEFAULT CHARACTER SET = utf8mb4;"""

        master_user = "INSERT INTO `jc_vidros`.`usuarios` (`nome`, `user`, `senha`, `perfil`) VALUES ('Master', 'Admin', 'Admin', 'Administrador');"

        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Confirmar Acao")
        msg.setText("ESTA ACAO EXCLUIRA TODOS OS USUARIOS,"
                    "DESEJA CONFIRMAR ACAO??")
        msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        exec = msg.exec_()

        if exec == QtWidgets.QMessageBox.Ok:

            try:
                cursor.execute(apagar_usuarios)
                cursor.execute(criar_usuarios)
                cursor.execute(master_user)
                con.commit()

            except Error as error:
                print(f"Erro ao Apagar Usuarios: {error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"""Erro Ao Apagar Usuarios
                                            {error}""")
                msg.exec_()

            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Usuarios Apagados")
                msg.setText("Usuarios Apagados Com Sucesso")
                msg.exec_()

        else:
            print("Acao Cancelada")

    def cadastro_usuario(self):
        nome = self.lineEdit_6.text()
        user = self.lineEdit_5.text()
        senha = self.lineEdit_4.text()
        perfil = self.combo_perfil_user_2.currentText()

        inserir = f"INSERT INTO `jc_vidros`.`usuarios` (`nome`, `user`, `senha`, `perfil`) VALUES ('{nome}', '{user}', '{senha}', '{perfil}');"

        if con.is_connected():
            try:
                cursor.execute(inserir)
                con.commit()

            except Error as error:
                print(f"Erro ao Inserir Usuarios: {error}")
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Warning)
                msg.setWindowTitle("Error")
                msg.setText(f"""Erro Ao Inserir Usuarios
                                                       {error}""")
                msg.exec_()

            finally:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Question)
                msg.setWindowTitle("Usuario Cadastrado")
                msg.setText("Usuarios Cadastrado Com Sucesso")
                msg.exec_()

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


#tela_inserir = uic.loadUi('tela_inserir.ui')
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    alt_cliente = uic.loadUi("alterar_clientes.ui")
    excluir_cliente = uic.loadUi("excluir_clientes.ui")
    inserir_cliente = uic.loadUi("inserir_clientes.ui")
    login = Login()
    login.show()
    #w = MainWindow()
    # w.show()
    sys.exit(app.exec_())
