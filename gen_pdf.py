from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4



def mm(milimetros):
    return milimetros / 0.1





# doc = SimpleDocTemplate('../../../../Desktop/PDF.pdf', pagesize=letter)
# #container for the 'Flowable' objects
# elements = []
def gen_pdv():
    cod = 15
    cliente = "Carlos"
    endereco = "Rua Whasingthon Luis"
    bairro = "Neves"
    estado = "RJ"
    cidade = "SG"
    cep = 00000 - 000
    qt = 1
    alt = 2.1
    lar = 0.7
    val = 600
    prec = 1000

    c = canvas.Canvas('../../../Desktop/PDF.pdf')

    c.setFont("Times-Roman", 20)
    c.drawString(400, 200,"Orçamento")

    c.setFont("Times-Roman", 16)
    c.drawString(100, 200, "JC_VIDROS")

    c.setFont("Times-Roman", 12)
    c.drawString(50, 170 ,"Rua Visconde De Itauna 1638")

    c.drawString(50,145, "(21)96968-4788")
    c.drawString(150,145, "(21)99434-2082")
    c.drawString(250,145, "Email: carlosaugusto270475@gmail.com")
    c.line(50, 140, 550, 140)
    c.drawString(50,130, f"Cliente:       {cod}           {cliente}")
    c.line(50, 127, 550, 127)
    c.drawString(50, 120, f"Endereço:  {endereco}              Bairro:   {bairro}          UF:{estado}")
    c.line(50,115,550,115)
    c.drawString(50, 105, f"Cidade:  {cidade}    CEP:{cep}")
    c.line(50,100,550,100)
    c.drawString(50, 80, "Codigo     Nome                QT      Altura          Largura         Val.Un          Preco")
    #c.drawString(50, 70, f"{cod}")

    x = 50

    list = [f"{cod, cliente, qt, alt, lar, val, prec}"]
    new = []
    for b in list:
        b = b.replace("(","").replace(")","").replace("\'", "")
        c.drawString(x, 70, b)
        x =+ 100


    print("Documento Gerado")
    c.save()

#data= [['Codigo', 'Nome', 'QT', 'Altura', 'Largura','Val Un.', 'Preço']]
# # ['Val Un.', 'Preço']]
#
# t = Table(data)
#
#
# # style = TableStyle([('BACKGROUND',(1,1),(-2,-2),colors.green),
# # ('TEXTCOLOR',(0,0),(1,-1),colors.red)])
# #
# # t.setStyle(style)
#
# elements.append(t)
# # write the document to disk
# doc.build(elements)