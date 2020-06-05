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
from PySide2.QtWidgets import QMainWindow, QFileDialog, QWidget, QVBoxLayout, QGraphicsScene, QGraphicsView
from PySide2 import QtCore, QtGui, QtWidgets


import sys,os,ntpath,ctypes
import tkinter as tk
from tkinter import filedialog



class Ui_ELF_Upload(object):
    def setupUi(self, ELF_Upload):
        if ELF_Upload.objectName():
            ELF_Upload.setObjectName(u"ELF_Upload")
        ELF_Upload.setEnabled(True)
        ELF_Upload.resize(601, 334)
        self.setIconModes(ELF_Upload)
        
        
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
        
        self.setIcon(ELF_Upload)
       

    # setupUi
    
    def setIcon(self,ELF_Upload):
      appIcon = QIcon("icon.png")
      ELF_Upload.setWindowIcon(appIcon)
      
    def setIconModes(self,ELF_Upload):
        icon = QtGui.QPixmap("icon.png")
        label = QtWidgets.QLabel('Sample', ELF_Upload)
        pixmap = icon.scaled(601, 334, QtCore.Qt.KeepAspectRatio) 
        label.setPixmap(pixmap)    
        label.show()
        '''
        icon2 = QIcon("icon.png")
        label2 = QLabel('Sample', ELF_Upload)
        pixmap2 = icon2.pixmap(1000, 1000, QIcon.Disabled, QIcon.Off)
        label2.setPixmap(pixmap2)
        label2.move(100,0)
        '''
    
    def Browse_Handler(self):
      global file_path
      root = tk.Tk()
      root.withdraw()
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Elf files","*.elf"),("all files","*.*")))
      file_path = root.filepath


    def Upload_Handler(self):
      os.system('upload-script.py'+' '+str(file_path))   #TODO
      ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)
      os.system('progress.py')


    def retranslateUi(self, ELF_Upload):
        ELF_Upload.setWindowTitle(QCoreApplication.translate("ELF_Upload", u"FOTA PC-GUI", None))
        self.upload_pushButton.setText(QCoreApplication.translate("ELF_Upload", u"Upload", None))
        self.Browse_pushButton.setToolTip(QCoreApplication.translate("ELF_Upload", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">Browse</span></p></body></html>", None))
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



