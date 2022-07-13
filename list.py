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
nome = "diego"
orcamento = 12
bairro = "gradim"
cidade = "SG"
endereco = "Rua rosalina"
estado = "RJ"
projeto = "porta"
telefone = 39202
celular = 820828


dados_cliente =  '\'' + str(nome) + '\'' + ',\'' + str(orcamento) + '\'' + ',\'' + str(bairro) + '\'' + ',\'' + str(
    cidade) + '\'' + ',\'' + str(endereco) + '\'' + ',\'' + str(estado) + '\'' + ',\'' + str(
    telefone) + '\'' + ',\'' + str(celular) + '\'' + ');'


declaracao = f"""insert into clientes
                         (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
                         values
                         ('{nome}', '{orcamento}', '{bairro}', '{cidade}', '{endereco}', '{estado}', '{telefone}', '{celular}')"""

declaracao_2 = f"""insert into clientes
                             (cliente, orcamento, bairro, cidade, endereco, uf, telefone, celular)
                             values
                             ({dados_cliente}"""




print(declaracao)
print(declaracao_2)