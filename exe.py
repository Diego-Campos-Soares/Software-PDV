from gui import *
import mysql.connector
from mysql.connector import Error
import sys


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

        self.btn_avancar.clicked.connect(self.valores_cliente)

    def valores_cliente(self):
        cod = self.box_cliente.value()
        nome = self.line_cliente.text()
        orcamento = self.line_orcamento.text()
        bairro = self.line_bairro.text()
        cidade = self.line_cidade.text()
        endereco = self.line_endereco.text()
        estado = self.line_estado.text()
        projeto = self.box_projeto.value()
        telefone = self.line_telefone.text()
        celular = self.line_celular.text()



        dados_cliente = '\'' + str(nome) + '\'' + ',\'' + str(orcamento) + '\''  + ',\'' + str(bairro) + '\'' + ',\'' + str(cidade) + '\'' + ',\'' + str(endereco) + '\'' + ',\'' + str(estado) + '\'' + ',\'' + str(projeto) + '\'' ',\'' + str(telefone) + '\'' + ',\'' + str(celular) + '\'' + ');'

        declaracao = f"""insert into clientes
                            (cliente, orcamento, bairro, cidade, endereco, uf, projeto, telefone, celular)
                            values 
                            ({dados_cliente}"""  
    


        

        try:
            con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")

            if con.is_connected():
                db_info = con.get_server_info()
                print("conectado ao servidor msql versao", db_info)

            cursor = con.cursor(buffered=True)
            cursor.execute("select database();")
            cursor.execute(declaracao)
            print(declaracao)
            con.commit()
            

        except Error as erro:
            print("falha ao inserir dados no MySQL: {}".format(erro))

        finally:
            if con.is_connected():
                cursor.close()
                con.close()
                print("Conexao ao MySql foi encerrada")

    def valores_produto(self):
        self.box_produto = self.box_produto.value()
        self.quantidade = self.box_quantidade.value()
        self.altura = self.box_altura.value()
        self.largura = self.box_largura.value()

        print(self)


#var = MainWindow
#fun = var.valores_cliente
#valor = fun.get_dados_cliente

#print(fun)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())
