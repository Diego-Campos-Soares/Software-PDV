import mysql.connector
from mysql.connector import Error


class Data_base:
    def __init__(self, name='jc_vidros') -> None:
        self.name = name
        self.con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
        if self.con.is_connected():
            db_info = self.con.get_server_info()
            print("conectado ao servidor msql versao", db_info)

    def close(self):
        try:
            self.con.close()
        except:
            pass

############ USUARIOS   ##############

    def create_user(self):
        c = self.con.cursor(buffered=True)
        c.execute(f"""CREATE TABLE `jc_vidros`.`usuarios` (
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
                                DEFAULT CHARACTER SET = utf8mb4;""")

        c.execute("INSERT INTO `jc_vidros`.`usuarios` (`nome`, `user`, `senha`, `perfil`) VALUES ('Master', 'Admin', 'Admin', 'Administrador');")

        self.con.commit()

    def drop_user(self):
        c = self.con.cursor(buffered=True)
        c.execute(f"""DROP TABLE IF EXISTS usuarios""")
        self.con.commit()

    def select_user(self, user):
        c = self.con.cursor(buffered=True)
        c.execute(f"""SELECT user, senha, perfil FROM usuarios WHERE user='{user}'""")
        result = c.fetchall()
        return result

    def insert_user(self, nome, email, user, senha, perfil):
        c = self.con.cursor(buffered=True)
        c.execute(f"INSERT INTO `jc_vidros`.`usuarios` (`nome`, `email`, `user`, `senha`, `perfil`) VALUES ('{nome}', '{email}', '{user}', '{senha}', '{perfil}');")
        self.con.commit()

######### CLIENTES  ################

    def create_clientes(self):
        c = self.con.cursor(buffered=True)
        c.execute("""CREATE TABLE IF NOT EXISTS`jc_vidros`.`clientes` (
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
        DEFAULT CHARACTER SET = utf8mb4;""")

    def select_cliente(self):
        c = self.con.cursor()
        c.execute("select * from clientes")
        clientes = c.fetchall()
        return clientes

    def insert_cliente(self, nome , orcamento, bairro, cidade, endereco, estado, telefone, celular, resumed):
        c = self.con.cursor(buffered=True)
        c.execute(f"""insert into clientes
                 (cliente, orcamento, bairro, cidade, endereço, uf, telefone, celular, data)
                 values
                 ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}', '{resumed}')""")
        self.con.commit()

    def drop_clientes(self):
        c =self.con.cursor(buffered=True)
        c.execute(f"DROP TABLE CLIENTES")
        self.con.commit()

    def excluir_cliente(self, cliente):
        c = self.con.cursor(buffered=True)
        c.execute(f"SELECT cliente from clientes WHERE cliente = '{cliente}'")
        result = c.fetchone()
        cliente_db = result.replace("()", "")

        if result[0] == cliente:
            c.execute(f"DELETE from clientes WHERE cliente = '{cliente}'")
            self.con.commit()
        elif result[0] != cliente:
            print("Cliente Invalido")
        else:
            print("E ai")


############ PRODUTOS   ###############

    def select_all_produto(self):
        c = self.con.cursor()
        c.execute("select * from produtos")
        produtos = c.fetchall()
        return produtos

    def insert_produto(self, cod, produto, desc, alt, lar, val, com):
        c = self.con.cursor()
        c.execute(f"""INSERT INTO produtos
                (id, produto, descricao, altura, largura, valor, comprimento)
                VALUES
                ('{cod}','{produto}','{desc}','{alt}','{lar}','{val}','{com}')""")
        self.con.commit()

    def drop_produto(self):
        c = self.con.cursor()
        c.execute("DROP TABLE produtos")
        self.con.commit()

    def create_produto(self):
        c = self.con.cursor()
        c.execute(f"""CREATE TABLE IF NOT EXISTS `produtos` (
                                         `id` INT(11) NOT NULL,
                                         `produto` VARCHAR(45) NULL,
                                         `descricao` VARCHAR(60) NULL,
                                         `altura` DECIMAL(4,2) NULL,
                                         `largura` DECIMAL(4,2) NULL,
                                         `valor` DECIMAL(6,2) NULL,
                                         `comprimento` DECIMAL(4,2) NULL,
                                          PRIMARY KEY (id)
                                         )DEFAULT CHARACTER SET = utf8mb4;""")

        self.con.commit()

    def select_valor(self, produto):
        c = self.con.cursor()
        c.execute(f"""SELECT valor FROM produtos WHERE ID= '{produto}'""")
        result = c.fetchone()
        return result

    def select_produto(self, cod):
        c = self.con.cursor()
        c.execute(f"""SELECT produto FROM produtos WHERE ID ={cod}""")
        result = c.fetchone()
        return result

############


