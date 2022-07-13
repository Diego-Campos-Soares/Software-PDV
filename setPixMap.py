import gui
from PyQt5 import QtGui
def index_modelo(self):
    modelo = self.combo_modelo.currentIndex()
    if modelo == 0:
        self.img_projeto.clear()
    elif modelo == 1:
        self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE.PNG"))
    elif modelo == 2:
        self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 1 FIXO.png"))
    elif modelo == 3:
        self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS.png"))
    elif modelo == 4:
        self.img_projeto.setPixmap(QtGui.QPixmap("resized/PORTA PIVOTANTE 2 FOLHAS 2 FIXOS.png"))








# imagems = [
#     "resized/PORTA PIVOTANTE.PNG",
#     "resized/PORTA PIVOTANTE 1 FIXO.png",
#     "resized / PORTA PIVOTANTE 2 FOLHAS.png",
#     "resized/PORTA PIVOTANTE 2 FOLHAS 2 FIXOS.png"
# ]
# for i in imagems:
#     self.img_projeto.setPixMap(QtGui.QPixmap(""))
