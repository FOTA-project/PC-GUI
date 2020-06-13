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

import sys, time, os

INSTRUCTION_WRITE_MAX_REQUESTS    = -4
INSTRUCTION_COMM_TIMEOUT          = -2
INSTRUCTION_TERMINATE_ON_SUCCESS  = -3

class Ui_Form(object):
    def setupUi(self, Form):
        if Form.objectName():
            Form.setObjectName(u"Flashing progress")
        Form.resize(519, 124)

        self.progressBar = QProgressBar(Form)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(80, 60, 401, 41))
        self.progressBar.setMinimum(0)
        #self.progressBar.setMaximum(700)
        
        self.worker = Worker()
        self.worker.updateProgress.connect(self.setProgress)
        self.worker.start()
        self.retranslateUi(Form)
        
        QMetaObject.connectSlotsByName(Form)
        
        self.setIcon(Form)
    # setupUi
    
    def setIcon(self,GUI):
        appIcon = QIcon("icon.png")
        GUI.setWindowIcon(appIcon)
    
    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Flashing progress", None))
        self.progressBar.setValue(0)
   # retranslateUi
    
    def setProgress(self, progress, max):
        self.progressBar.setMaximum(max)
        self.progressBar.setValue(progress)


#Inherit from QThread
class Worker(QtCore.QThread):

    #This is the signal that will be emitted during the processing.
    #By including int as an argument, it lets the signal know to expect
    #an integer argument when emitting.
    updateProgress = QtCore.Signal(int, int)

    #You can do any extra things in this init you need, but for this example
    #nothing else needs to be done expect call the super's init
    def __init__(self):
        QtCore.QThread.__init__(self)

    #A QThread is run by calling it's start() function, which calls this run()
    #function in it's own "thread". 
 
    def run(self):
        global f
        #Notice this is the same thing you were doing in your progress() function
        
        #self.updateProgress.emit(progress)
        '''
        for i in range(1, 101):
            #Emit the signal so it can be received on the UI side.
            self.updateProgress.emit(i)
            time.sleep(0.1)
        '''
        f = open('progress.txt', 'w+')
        #f = os.fdopen(os.open('progress.txt', os.O_RDWR | os.O_CREAT), 'w+')
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
                Widget.close()
                print("Widget.close() ------ 1\n")
                #f.close()
            elif int(progress[:2], 10) == INSTRUCTION_TERMINATE_ON_SUCCESS:
                Widget.close()
                print("Widget.close() ------ 2\n")
                #f.close()
                ##
            else: # normal number
                self.updateProgress.emit(int(progress), int(maxRequests))
                #Form.setProgress( int(progress) )
                print("progress.py: progress = %d\n" %(int(progress)))
                time.sleep(0.000001 * 500) # 500us
                
            #f = open('progress.txt', 'w')
            #f.write('0')


app=QApplication(sys.argv)   #create app and return handeler but it need list of argv
Widget=QWidget()  # create widget
Form=Ui_Form()  # create form
Form.setupUi(Widget)   # to create form inside widget
Widget.show()
sys.exit(app.exec_()) 
