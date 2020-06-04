# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'progress.ui'
##
## Created by: Qt User Interface Compiler version 5.14.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2 import QtCore
from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *

from PySide2.QtWidgets import QApplication, QMainWindow, QProgressBar, QStatusBar, QLabel
import sys
from PySide2.QtGui import QIcon

import sys,time

class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(519, 124)
        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(80, 60, 401, 41))
     
        
        #self.statusLabel = QLabel("Showing Progress")
        #self.progressBar = QProgressBar()
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(100)
        
        #self.createStatusBar()
        
        self.worker = Worker()
        self.worker.updateProgress.connect(self.setProgress)
        self.worker.start()
        self.retranslateUi(Form)
        
        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
        self.progressBar.setValue(0)
   # retranslateUi
    
    def setProgress(self, progress):
        self.progressBar.setValue(progress)
        
    def createStatusBar(self):
        #self.statusBar = QStatusBar()
        self.progressBar.setValue(50)
        #self.statusBar.addWidget(self.statusLabel, 1)
        #self.statusBar.addWidget(self.progressBar, 2)
        #self.setStatusBar(self.statusBar)

#Inherit from QThread
class Worker(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    updateProgress = QtCore.Signal(int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self):
        QtCore.QThread.__init__(self)

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread". 
 
    def run(self):
        #Notice this is the same thing you were doing in your progress() function
        
        #self.updateProgress.emit(progress)
        '''
        for i in range(1, 101):
            #Emit the signal so it can be received on the UI side.
            self.updateProgress.emit(i)
            time.sleep(0.1)
        '''
        progress_int=0
        while progress_int != 100:
            f=open('progress.txt', 'r')
            progress=f.readline()
            f.close()
            progress_int=int(progress.strip())
            self.updateProgress.emit(progress_int)
            time.sleep(0.75)
            
            
app=QApplication(sys.argv)   #create app and return handeler but it need list of argv
Widget=QWidget()  # create widget
Form=Ui_Form()  # create form
Form.setupUi(Widget)   # to create form inside widget
Widget.show()
sys.exit(app.exec_()) 
