from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from tkinter import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUiType
import sys

zi,_ = loadUiType('Widgets/Customer_care.ui')
class Care(QMainWindow,zi):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Care")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        # self.showMaximized()
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.close_button.clicked.connect(self.Exit)
        self.show()

        
        
    def Exit(self):
        self.close()
        
 
