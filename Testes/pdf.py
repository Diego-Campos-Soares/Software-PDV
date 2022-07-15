import webbrowser

import PyPDF2
import decorator
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from PyPDF2 import *
import re
import webbrowser

cliente = "Carlos"

# file = open('../../../../Desktop/PDF.pdf', 'rb')
# reader = PyPDF2.PdfFileReader(file)
# merger = PyPDF2.PdfFileMerger()
#
#
# pg1 = reader.getPage(0)
# txt1 = pg1.extractText()
# txt2 = re.sub('\n', '', txt1)
# txt3 = re.sub('Nome_do_cliente', cliente, txt2)
#
# merger.write('../../../../Desktop/NewPDF.pdf')
# print(txt1)
# print(txt2)
#print(txt3)





# print(txt3)


c = canvas.Canvas('../../../../Desktop/PDF.pdf')
#pg= c.getpdfdata()

#pg.re.sub('Orçamento', cliente, pg)
c.drawString(400, 200 ,"Orçamento")
c.setFont("Times-Bold", 24)
c.drawString(100, 250, "JC_VIDROS")
c.setFont("Times-Roman", 12)
c.drawString(50, 170 ,"Rua Visconde De Itauna 1638")
c.drawString(50,150, "(21)9999999")
c.line(100, 150, 200, 150)
c.save()
