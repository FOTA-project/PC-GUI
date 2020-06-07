# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ELf.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *
from PySide2 import QtCore, QtGui, QtWidgets


import sys,os,ntpath,ctypes
import tkinter as tk
from tkinter import filedialog

import threading
import subprocess

import time


file_path = ''

def progress_script_thread():
    os.system('progress-script.py')

def progress_thread():
    os.system('progress.py')

class Ui_GUI(object):
    def setupUi(self, GUI):
        if GUI.objectName():
            GUI.setObjectName(u"GUI")
        GUI.setEnabled(True)
        GUI.resize(552, 300)
        
        self.setIconModes(GUI)
        
        palette = QPalette()
        brush = QBrush(QColor(255, 255, 255, 255))
        brush.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Active, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Active, QPalette.Button, brush)
        palette.setBrush(QPalette.Active, QPalette.Base, brush)
        palette.setBrush(QPalette.Active, QPalette.Window, brush)
        palette.setBrush(QPalette.Inactive, QPalette.WindowText, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Button, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Base, brush)
        palette.setBrush(QPalette.Inactive, QPalette.Window, brush)
        brush1 = QBrush(QColor(120, 120, 120, 255))
        brush1.setStyle(Qt.SolidPattern)
        palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush1)
        palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
        palette.setBrush(QPalette.Disabled, QPalette.Window, brush)
        GUI.setPalette(palette)
        GUI.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.upload_pushButton = QPushButton(GUI)
        self.upload_pushButton.setObjectName(u"upload_pushButton")
        self.upload_pushButton.setGeometry(QRect(350, 220, 181, 41))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75);
        self.upload_pushButton.setFont(font)
        self.upload_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.Browse_pushButton = QPushButton(GUI)
        self.Browse_pushButton.setObjectName(u"Browse_pushButton")
        self.Browse_pushButton.setGeometry(QRect(350, 140, 181, 41))
        self.Browse_pushButton.setFont(font)
        self.Browse_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.comboBox = QComboBox(GUI)
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(350, 70, 181, 41))
        self.comboBox.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.comboBox.setEditable(False)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75);
        self.comboBox.setFont(font)
        self.label = QLabel(GUI)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(350, 20, 181, 21))
        font1 = QFont()
        font1.setPointSize(10)
        font1.setBold(True)
        font1.setWeight(75);
        self.label.setFont(font1)

        self.retranslateUi(GUI)

        QMetaObject.connectSlotsByName(GUI)
        
        
        ## we edit here 
        self.upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)
        
        self.setIcon(GUI)
    # setupUi
    
    
    def setIcon(self,GUI):
        appIcon = QIcon("icon.png")
        GUI.setWindowIcon(appIcon)
      
    def setIconModes(self,GUI):
        icon = QtGui.QPixmap("icon.png")
        label = QtWidgets.QLabel('Sample', GUI)
        pixmap = icon.scaled(601, 334, QtCore.Qt.KeepAspectRatio) 
        label.setPixmap(pixmap)    
        label.show()
        
    def Browse_Handler(self):
      global file_path
      root = tk.Tk()
      root.withdraw()
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("Elf files","*.elf"),("all files","*.*")))
      file_path = root.filepath

    def Upload_Handler(self):
        os.system('upload-script.py' + ' ' + str(file_path))   #TODO
        ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)
        #os.system('progress.py')
        time.sleep(1)
        
        #processThread = threading.Thread(target=progress_script_thread)
        #processThread.start()
        
        progressScriptThreadHandle = threading.Thread(target=progress_script_thread)
        progressThreadHandle = threading.Thread(target=progress_thread)
        
        time.sleep(13)
        progressScriptThreadHandle.start()
        time.sleep(1)
        progressThreadHandle.start()
        
        #time.sleep(1)

        #os.system('progress.py')
        #progress_script_thread()
        
        #processThread.stop()
        #os.system('upload-script.py'+' '+str(file_path))   #TODO
    
    def retranslateUi(self, GUI):
        GUI.setWindowTitle(QCoreApplication.translate("GUI", u"FOTA PC-GUI", None))
        self.upload_pushButton.setText(QCoreApplication.translate("GUI", u"Upload", None))
#if QT_CONFIG(tooltip)
        self.Browse_pushButton.setToolTip(QCoreApplication.translate("GUI", u"<html><head/><body><p align=\"center\"><span style=\" font-size:24pt; font-weight:600;\">Browse</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.Browse_pushButton.setText(QCoreApplication.translate("GUI", u"Browse", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("GUI", u"STM32", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("GUI", u"ATmega32", None))

        self.comboBox.setCurrentText(QCoreApplication.translate("GUI", u"STM32", None))
        self.label.setText(QCoreApplication.translate("GUI", u"Microcontrollers ", None))
    # retranslateUi



app=QApplication(sys.argv)   #create app and return handeler but it need list of argv
Widget=QWidget()  # create widget
Form=Ui_GUI()  # create form
Form.setupUi(Widget)   # to create form inside widget
Widget.show()
sys.exit(app.exec_()) 
