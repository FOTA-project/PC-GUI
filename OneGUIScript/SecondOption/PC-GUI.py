# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PC-GUI.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,QThread,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from PySide2 import QtCore, QtGui, QtWidgets


import sys,os,ntpath,ctypes
import tkinter as tk
from tkinter import filedialog
from tkinter import *

#import ProgressScript,UploadScript

import threading
import subprocess

import sys, time, os
import progress_script
import upload_script

file_path = ''

INSTRUCTION_WRITE_MAX_REQUESTS    = -4
INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

STOP_THREAD_FLAG=0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(552, 301)
        font = QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75);
        MainWindow.setFont(font)
        MainWindow.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Browse_pushButton = QPushButton(self.centralwidget)
        self.Browse_pushButton.setObjectName(u"Browse_pushButton")
        self.Browse_pushButton.setGeometry(QRect(420, 120, 112, 41))
        self.Browse_pushButton.setFont(font)
        self.Browse_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.Upload_pushButton = QPushButton(self.centralwidget)
        self.Upload_pushButton.setObjectName(u"Upload_pushButton")
        self.Upload_pushButton.setGeometry(QRect(420, 190, 112, 41))
        self.Upload_pushButton.setFont(font)
        self.Upload_pushButton.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.comboBox = QComboBox(self.centralwidget)
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        self.comboBox.addItem(str())
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(420, 60, 111, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.comboBox.setFont(font1)
        self.comboBox.setStyleSheet(u"background-color: rgb(97, 144, 200);")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(410, 20, 111, 20))
        self.label.setFont(font)
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(10, 10, 391, 221))
        self.frame.setStyleSheet(u"image: url(icon.png);")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(18, 239, 81, 31))
        self.label_2.setFont(font)
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(260, 240, 291, 31))
        #self.progressBar.setValue(24)
        self.lineEdit = QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(105, 240, 140, 31))
        self.lineEdit.setFont(font1)
        self.lineEdit.setReadOnly(True)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
        
        ## we edit here 
        self.Upload_pushButton.clicked.connect(self.Upload_Handler)
        self.Browse_pushButton.clicked.connect(self.Browse_Handler)
        self.setIcon(MainWindow)
        self.worker = Worker()
    # setupUi

    def setIcon(self,MainWindow):
        appIcon = QIcon("icon.png")
        MainWindow.setWindowIcon(appIcon)
    
    def Browse_Handler(self):
      global file_path
      root = tk.Tk()
      root.withdraw()
      root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='icon.png'))
      root.filepath = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetype= ([("Elf files","*.elf")]))
      file_path = root.filepath

    def Upload_Handler(self):
        global user
        user = self.comboBox.currentIndex()
        
        
        global state
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Uploading.....", None))
        state=upload_script.UploadElfFile(file_path,user)
        
        if state == 1: #There is an error
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Error.. ", None))
            #TODO:program should exit
            #value=ctypes.windll.user32.MessageBoxW(0, "Done!", "uploaded to server", 1)
        else:
            self.progressBar.setMaximum(100)
            self.progressBar.setValue(100)
            time.sleep(1)
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Upload done ", None))
            self.progressBar.reset()
            
            #progress-script.py
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u" Flashing.....", None))
            #progressScriptThreadHandle = threading.Thread(target=progress_script.ReadProgress(user))

            #time.sleep(13)
            #progressScriptThreadHandle.start()
            #time.sleep(1)
        
            #progress.py
            self.worker.updateProgress.connect(self.setProgress)
            self.worker.start()
            
       
  
    def setProgress(self, progress, max):
        #print('Progress = '+str(progress))
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(progress)
        if progress >= max:
            self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"  Flash done", None))
            self.worker.stop()

    
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"FOTA PC-GUI", None))
        self.Browse_pushButton.setText(QCoreApplication.translate("MainWindow", u"Browse", None))
        self.Upload_pushButton.setText(QCoreApplication.translate("MainWindow", u"Upload", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"USER_1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"USER_2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("MainWindow", u"USER_3", None))

        self.label.setText(QCoreApplication.translate("MainWindow", u"    USERS", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"  Status", None))
        self.lineEdit.setText(QCoreApplication.translate("MainWindow", u"        Idle", None))
    # retranslateUi

class Worker(QtCore.QThread):
    updateProgress = QtCore.Signal(int, int)
    def __init__(self):
        QtCore.QThread.__init__(self)
    
    def run(self):
        global f
        f = open('progress.txt', 'r')
        f.seek(0)
        progress = 0
        maxRequests = -1
        
        while progress != maxRequests:
            progress = f.readline().strip()
            f.flush()
            
            if progress == '':
                time.sleep(0.000001 * 500) # 500us
                continue
            elif int(progress[:2], 10) == INSTRUCTION_WRITE_MAX_REQUESTS:
                maxRequests = int(progress.split()[1])
                print("progress.py: maxRequests = %d\n" %(maxRequests))
            elif int(progress[:2], 10) == INSTRUCTION_COMM_TIMEOUT:
                # TODO handle this
                #SecondWindow.close()
                print("Widget.close() ------ 1\n")
                #f.close()
            elif int(progress[:2], 10) == INSTRUCTION_TERMINATE_ON_SUCCESS:
                #SecondWindow.close()
                print("Widget.close() ------ 2\n")
                
                #f.close()
                ##
            else: # normal number
                self.updateProgress.emit(int(progress), int(maxRequests))
                #Form.setProgress( int(progress) )
                print("progress.py: progress = %d\n" %(int(progress)))
                #time.sleep(0.000001 * 500) # 500us
                
            #f = open('progress.txt', 'w')
            #f.write('0')
    
    def stop(self):
        print()
        self.requestInterruption()
        self.terminate()
        
        

app = QApplication(sys.argv)
window = QMainWindow()
Form=Ui_MainWindow()
Form.setupUi(window)
window.show()
sys.exit(app.exec_())

