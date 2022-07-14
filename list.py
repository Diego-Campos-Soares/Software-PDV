import mysql.connector


con = mysql.connector.connect(host="localhost", database="jc_vidros", user="root", password="")
cursor = con.cursor(buffered=True)
if con.is_connected():
    db_info = con.get_server_info()
    print("conectado ao servidor msql versao", db_info)


portas = [
    ("PROJETO SEM IMAGEM"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE 1 FIXO"),
    ("PORTA PIVOTANTE 2 FOLHAS"),
    ("PORTA PIVOTANTE 2 FOLHAS 2 FIXO"),
    ("PORTA PIVOTANTE 1 FIXO 1 BANDEIRA"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE"),
    ("PORTA PIVOTANTE")

]
janelas = [
    ("PROJETO SEM IMAGEM"),
    ("JANELA 1 FOLHA MOVEL 1 FIXO"),
    ("JANELA 2 FOLHAS MOVEL"),
    ("JANELA 2 FOLHA MOVEL 1 FIXA")
]



##########################################        clientes      #######################################################
nome = "diego"
orcamento = 14
bairro = "gradim"
cidade = ""
endereco = "Rua rosalina"
estado = ""
projeto = "porta"
telefone = 75475457
celular = 64462642

# inserir_clientes = f"""insert into clientes
#                          (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
#                          values
#                          ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}')"""
#
# consultar_clientes = """SELECT * FROM clientes"""
#
#
# if con.is_connected():
#     cursor.execute(inserir_clientes)
#     cursor.execute(consultar_clientes)
#     result = cursor.fetchall()
#     print(result)
#     print(inserir_clientes)
#     con.commit()




##########################################        orcamentos      #######################################################
# produto = 12
# quantidade = 3
# altura = 4
# largura = 2
#
# inserir_orcamento = f"""insert into orcamento
#         (produto, quantidade, altura, largura)
#         values
#         ('{produto}', '{quantidade}', '{altura}', '{largura}')"""
#
# consultar_orcamento = """SELECT * FROM orcamento"""
#
# if con.is_connected():
#     cursor.execute(inserir_orcamento)
#     cursor.execute(consultar_orcamento)
#     result = cursor.fetchall()
#     print(result)
#     con.commit()

declaracao = f"""insert into clientes
                                (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
                                values
                                ('{nome}','{orcamento}','{bairro}', '{cidade}','{endereco}','{estado}','{telefone}','{celular}') """
if con.is_connected():
    cursor.execute(declaracao)
    print(declaracao)
    con.commit()

if con.is_connected():
    con.close()
    print("connexao encerrada")