from email.mime import image
from tkinter import image_names
from PyQt5.QtWidgets import QTableWidgetItem, QWidget, QMessageBox, QFileDialog
from PyQt5 import QtGui, QtWidgets, QtCore
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import mysql.connector
from mysql.connector import Error
import re
import sys
from datetime import datetime, time
from datetime import date
#import pandas as pd
from glob import glob
from PIL import Image
from PIL.ImageQt import ImageQt
import os

# from datetime import datetime, time
# from datetime import date

# tempo = datetime.now()

# data = tempo.strftime("%x")

# hora = tempo.strftime("%X")

# resumed = data + " " + hora

# print(data)
# print(hora)
# print(resumed)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setMinimumSize(1000, 800)
        
        self.btn_open_file = QtWidgets.QPushButton(self)
        self.btn_open_file.setText("Open")
        self.btn_open_file.setGeometry(QtCore.QRect(440, 180, 41, 31))

        self.btn_add = QtWidgets.QPushButton(self)
        self.btn_add.setText("Add Projeto")
        self.btn_add.setGeometry(QtCore.QRect(440, 300, 41, 31))
        
        self.combo_modelo = QtWidgets.QComboBox(self)
        self.combo_modelo.setGeometry(QtCore.QRect(100, 190, 311, 21))
        
        self.produto = QtWidgets.QLabel(self)

        self.line_projeto = QtWidgets.QLineEdit(self)
        self.line_projeto.setGeometry(QtCore.QRect(100, 300, 311, 21))

        self.img = QtWidgets.QLabel(self)
        self.img.setGeometry(QtCore.QRect(100, 350, 400, 400))

        #self.btn_open_file.clicked.connect(self.openFile)
        self.btn_add.clicked.connect(self.add_projetos)

        
        
        self.combo_modelo.currentIndexChanged.connect(self.imageUpdate)
        
        
        self.path_arquivos()




      

    def add_projetos(self):
        projeto = self.line_projeto.text()
        lista = []
        lista.append(projeto)
        self.combo_modelo.addItems(lista)



    def setupUi(self, self1):
        pass

    def imageUpdate(self):
        imagePath       = "C:/Users/PC/PycharmProjects/pythonProject1/GIT_PDV/resized"
        #NewImagePath  =    self.openFile()
        currentItem     = str (self.combo_modelo.currentText ())
        currentImage    = '%s/%s.png'% (imagePath, currentItem)

        self.img.setPixmap(QtGui.QPixmap(currentImage))
        if self.btn_open_file.clicked:
            directory = QtWidgets.QFileDialog.getExistingDirectory()
            for _, _, arquivo in os.walk(directory):
                for items in arquivo:
                    final = items[:-4]
                    lista = [final]
                    self.combo_modelo.addItems(lista)
            currentNewImage = '%s/%s.png' % (directory, currentItem)
            self.img.setPixmap(QtGui.QPixmap(currentImage, currentNewImage))



    # def openFile(self, directory):
    #     directory = QtWidgets.QFileDialog.getExistingDirectory()
    #     for _, _, arquivo in os.walk(directory):
    #         for items in arquivo:
    #             final = items[:-4]
    #             lista = [final]
    #             self.combo_modelo.addItems(lista)
    #
    #     return directory



   
    def path_arquivos(self):
        for _, _, arquivo in os.walk('C:/Users/PC/PycharmProjects/pythonProject1/GIT_PDV/resized'):
            for i in arquivo:
                final = i[:-4]
                lista = [final]
        
                self.combo_modelo.addItems(lista)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())