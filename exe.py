
from gui import *
import mysql.connector
#from setPixMap import index_modelo
#import list
from PIL import Image
import sys


con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)
if con.is_connected():
    db_info = con.get_server_info()
    print("conectado ao servidor msql versao", db_info)

# portas = [
#     ("PROJETO SEM IMAGEM"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE 1 FIXO"),
#     ("PORTA PIVOTANTE 2 FOLHAS"),
#     ("PORTA PIVOTANTE 2 FOLHAS 2 FIXO"),
#     ("PORTA PIVOTANTE 1 FIXO 1 BANDEIRA"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE"),
#     ("PORTA PIVOTANTE")
#
# ]
# janelas = [
#     ("PROJETO SEM IMAGEM"),
#     ("JANELA 1 FOLHA MOVEL 1 FIXO"),
#     ("JANELA 2 FOLHAS MOVEL"),
#     ("JANELA 2 FOLHA MOVEL 1 FIXA")
# ]

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

       
        ########################    BOTOES DO SISTEMA   ##################################
        self.btn_avancar.clicked.connect(self.valores_cliente)
        self.btn_add.clicked.connect(self.valores_produto)

        ############################   PAGINAS DO SISTEMA   ##############################

        self.btn_PDV.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.PDV))
        self.btn_produtos.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Produtos))
        self.btn_caixa.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Caixa))
        self.btn_vendas.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Vendas))
        self.btn_cliente.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Clientes))
        self.btn_cliente.clicked.connect(self.mostrar_clientes)
        self.btn_Usuario.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.Usuario))

        ###########################     COMBO_BOX       ####################################
        self.combo_projeto.currentIndexChanged.connect(self.endereco_combo)
        self.combo_modelo.currentIndexChanged.connect(self.index_modelo)

        self.endereco_combo()

        # im = Image.open("resized/PORTA PIVOTANTE.png")
        # im.show(MainWindow)


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


    def valores_cliente(self):
        cod = self.box_cliente.value()
        nome = self.line_cliente.text()
        orcamento = self.line_orcamento.text()
        bairro = self.line_bairro.text()
        cidade = self.line_cidade.text()
        endereco = self.line_endereco.text()
        estado = self.line_estado.text()
        #projeto = self.combo_projeto.text()
        telefone = self.line_telefone.text()
        celular = self.line_celular.text()



        #dados_cliente = '\'' + str(nome) + '\'' + ',\'' + str(orcamento) + '\''  + ',\'' + str(bairro) + '\'' + ',\'' + str(cidade) + '\'' + ',\'' + str(endereco) + '\'' + ',\'' + str(estado) + '\'' + ',\'' + str(telefone) + '\'' + ',\'' + str(celular) + '\'' + ');'

        declaracao = f"""insert into clientes
                                 (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
                                 values
                                 ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}')"""

        if con.is_connected():
            cursor = con.cursor(buffered=True)
            cursor.execute(declaracao)
            print(declaracao)
            con.commit()
            
       
    def mostrar_clientes(self):
        cursor.execute("SELECT * FROM cliente")
        dados_lidos = cursor.fetchall()
        self.tabela_selecao_itens.setRowCount(len(dados_lidos))
        con.commit()
        print(dados_lidos)

    def valores_produto(self):
        produto = self.box_produto.value()
        quantidade = self.box_quantidade.value()
        altura = self.box_altura.value()
        largura = self.box_largura.value()
        
        valores = '\'' + str(produto) + '\'' + ',\'' + str(quantidade) + '\'' + ',\'' + str(altura) + '\'' + ',\'' + str(largura) + '\'' + ');'

        declaracao = f"""insert into orcamento
                            (produto, quantidade, altura, largura)
                            values 
                            ({valores}"""  
    

        if con.is_connected:
            cursor = con.cursor(buffered=True)
            cursor.execute(declaracao)
            cursor.execute("SELECT * FROM cliente")
            dados_lidos = cursor.fetchall()
            self.tabela_selecao_itens.setRowCount(len(dados_lidos))

            print(declaracao)
            con.commit()


    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    
    sys.exit(app.exec_())
    
