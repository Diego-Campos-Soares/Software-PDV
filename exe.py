from gui import *
import mysql.connector
from mysql.connector import Error
import sys

con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.setupUi(self)

       

        self.btn_avancar.clicked.connect(self.valores_cliente)
        self.btn_salvar.clicked.connect(self.valores_produto)

      
    def fechar_conexao():
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
        projeto = self.box_projeto.value()
        telefone = self.line_telefone.text()
        celular = self.line_celular.text()



        dados_cliente = '\'' + str(nome) + '\'' + ',\'' + str(orcamento) + '\''  + ',\'' + str(bairro) + '\'' + ',\'' + str(cidade) + '\'' + ',\'' + str(endereco) + '\'' + ',\'' + str(estado) + '\'' + ',\'' + str(projeto) + '\'' ',\'' + str(telefone) + '\'' + ',\'' + str(celular) + '\'' + ');'

        declaracao = f"""insert into clientes
                            (cliente, orcamento, bairro, cidade, endereco, uf, projeto, telefone, celular)
                            values 
                            ({dados_cliente}"""  
    


        

        

        if con.is_connected():
            db_info = con.get_server_info()
            print("conectado ao servidor msql versao", db_info)

       
            cursor = con.cursor(buffered=True)
            cursor.execute(declaracao)
            print(declaracao)
            con.commit()
            
       
        

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
            db_info = con.get_server_info()
            print("conectado ao servidor msql versao", db_info)

       
            cursor = con.cursor(buffered=True)
            cursor.execute(declaracao)
            print(declaracao)
            con.commit()
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    
    sys.exit(app.exec_())
    
