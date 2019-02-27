#!/usr/bin/env python
 
import sys, time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtCore import QThread

app = QApplication(sys.argv)

pages = [QWebView(), QWebView()]
pages[0].load(QUrl("http://sites.florianopolis.ifsc.edu.br/pecce/"))
pages[1].load(QUrl("http://www.florianopolis.ifsc.edu.br/"))

pages[0].showFullScreen()

index = 0

def task():
    global index
    index +=1
    pages[index%len(pages)].showFullScreen()
    pages[(index-1)%len(pages)].hide()

def updateSite():
    global pages
    for i in pages:
        i.reload()

timerW = QTimer()
timerU = QTimer()

if __name__ == '__main__':
    timerW.timeout.connect(task)
    timerU.timeout.connect(updateSite)
    timerW.start(10000)
    timerU.start(3600000)
    sys.exit(app.exec_())
