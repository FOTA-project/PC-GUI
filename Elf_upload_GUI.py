# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ELf.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt,SIGNAL)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
    
from PySide2.QtWidgets import *
#from PyQt5 import QtWidgets,QtCore, QtGui
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView
from PySide2 import QtCore, QtGui, QtWidgets
#from PySide2 import QtCore,  QFileDialog

import sys
import os 

import ntpath

import ctypes  # An included library with Python install.   



import tkinter as tk
from tkinter import filedialog


file_path = 0
fileName = 0


class Ui_ELF_Upload(object):
    def setupUi(self, ELF_Upload):
        if ELF_Upload.objectName():
            ELF_Upload.setObjectName(u"ELF_Upload")
        ELF_Upload.setEnabled(True)
        ELF_Upload.resize(601, 334)
        self.upload_pushButton = QPushButton(ELF_Upload)
        self.upload_pushButton.setObjectName(u"upload_pushButton")
        self.upload_pushButton.setGeometry(QRect(170, 230, 231, 41))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75);
        self.upload_pushButton.setFont(font)
        self.Browse_pushButton = QPushButton(ELF_Upload)
        self.Browse_pushButton.setObjectName(u"Browse_pushButton")
        self.Browse_pushButton.setGeometry(QRect(170, 160, 231, 41))
        self.Browse_pushButton.setFont(font)
        self.comboBox = QComboBox(ELF_Upload)
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(20, 50, 191, 41))
        self.comboBox.setEditable(False)
        self.label = QLabel(ELF_Upload)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 20, 181, 21))


        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75);
        self.label.setFont(font1)

        self.retranslateUi(ELF_Upload)

        QMetaObject.connectSlotsByName(ELF_Upload)

        ## we edit here 
        self.upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)

    # setupUi

    

    def Browse_Handler(self):
    	#fileName = QtGui.QFileDialog.getOpenFileName()
    	

    	#path_to_file, _ = QFileDialog.getOpenFileName(self, self.tr("Load Image"), self.tr("~/Desktop/"), self.tr("Images (*.jpg)"))
      global file_path
      global fileName
      root = tk.Tk()
      root.withdraw()
      file_path = filedialog.askopenfilename()
      fileName = ntpath.basename(str(file_path))
      #print (file_path)
      #print (str(fileName))

    	#fileName = QFileDialog.getOpenFileName(self,self.tr("Open File"), "/Users/pc/Desktop/ELF_GUI", self.tr("ELF Files (*.elf)"))
    	#self.ui.lineEdit.setText(fileName)


    def Upload_Handler(self):	

      print (str(fileName))
      print (file_path)
 
      os.system('upload-script.py'+' '+str(file_path))   #TODO
      ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)


    def retranslateUi(self, ELF_Upload):
        ELF_Upload.setWindowTitle(QCoreApplication.translate("ELF_Upload", u"Form", None))
        self.upload_pushButton.setText(QCoreApplication.translate("ELF_Upload", u"Upload", None))
#if QT_CONFIG(tooltip)
        self.Browse_pushButton.setToolTip(QCoreApplication.translate("ELF_Upload", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">Browse</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Browse_pushButton.setText(QCoreApplication.translate("ELF_Upload", u"Browse", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("ELF_Upload", u"STM32", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("ELF_Upload", u"ATmega32", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("ELF_Upload", u"STM32", None))
        self.label.setText(QCoreApplication.translate("ELF_Upload", u"Microcontrollers ", None))
        



app=QApplication(sys.argv)   #create app and return handeler but it need list of argv
Widget=QWidget()  # create widget
Form=Ui_ELF_Upload()  # create form
Form.setupUi(Widget)   # to create form inside widget
Widget.show()
sys.exit(app.exec_()) 


