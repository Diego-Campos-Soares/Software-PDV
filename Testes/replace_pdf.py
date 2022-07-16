import re
import PyPDF2
from reportlab.pdfgen import canvas

file = open('../../../../Desktop/PDF.pdf', 'rb')

reader = PyPDF2.PdfFileReader(file)

pg = reader.getPage(0)
txt = pg.extractText()
txt_re = re.sub('\n', '', txt)
txt2 = re.sub('Orçamento', 'Codigo',txt_re)



c = c = canvas.Canvas('../../../../Desktop/NewPDF.pdf')
c.drawString(100,100, txt2)
c.save()