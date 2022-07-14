from PyQt5.QtWidgets import QTableWidgetItem
from GIT_PDV.gui import *
import mysql.connector
import sys


con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)
if con.is_connected():
    db_info = con.get_server_info()
    print("conectado ao servidor msql versao", db_info)


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
        alt = self.box_altura_produto_2.value()
        lar = self.box_largura_produto_2.value()
        com = self.box_largura_produto_3.value()
        val = self.box_valor_produto_2.value()

        inserir_produtos = f"""INSERT INTO produtos
                (id, produto, descricao, altura, largura, valor, comprimento)
                VALUES
                ('{cod}','{produto}','{desc}','{alt}','{lar}','{val}','{com}')"""

        if con.is_connected():
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

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

