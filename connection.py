import sqlite3


class Data_base:
    def __init__(self, name="jc_vidros") -> None:
        self.name = name

    def connect(self):
        self.con = sqlite3.connect(self.name)

    def close(self):
        try:
            self.con.close()
        except:
            pass

    def create_clientes(self):
        c = self.con.cursor()
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

    def select_produto(self):
        c = self.con.cursor()
        c.execute("select * from produtos;")
        produtos = c.fetchall()
        print(produtos)


db = Data_base()
db.connect()
db.select_produto()
