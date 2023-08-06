from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QTimer
from tkinter import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUiType
import time
import sys
import Sales
import Purchase
import CustomerCare
import Return_Product
import Supplier
import Dashboard

fi,_ = loadUiType('Widgets/Flash_screen.ui')
class Screen(QMainWindow,fi):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Care")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.show()
        self.widget.setStyleSheet("background-image : url(assets/flash_wall.png);")   
        self.label_3.setStyleSheet("background-image : url(assets/icon03.png);")   
        self.timer=QTimer()
        self.timer.start(200)
        self.timer.timeout.connect(self.startProgress)
        
    def startProgress(self):
        for i in range(1, 100):
            time.sleep(0.008)
            self.progressBar.setValue(i)
            if(i==99):
                self.timer.stop()
                self.mainWindow = MainWindow()
                self.mainWindow.show()
                self.close()
                
                
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initUI()
        self.setWindowTitle('Home')
        self.showMaximized()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setGeometry(0, 0, 1366, 768)
        self.show()  
        
    def initUI(self):
        self.my_menubar()
        self.TabWindow()
        
        
    def my_menubar(self):
        self.menu_bar = self.menuBar()
        self.setStyleSheet("""
        QMainWindow{
            background-color: #1F1B24;                   
        }
        QMenuBar {
            background-color: #1F1B24;
            color: rgb(255,255,255);
            border: 1px solid #000;
            padding: 4px;
        }

        QMenuBar::item {
            background-color: #1F1B24;
            color: rgb(255,255,255);
        }

        QMenuBar::item::selected {
            background-color: rgb(30,30,30);
        }

        QMenu {
            background-color: rgb(49,49,49);
            color: rgb(255,255,255);
            border: 1px solid #000;           
        }

        QMenu::item::selected {
            background-color: rgb(30,30,30);
        }
    """)
        self.menu_bar.setCornerWidget
        icon_menu = self.menu_bar.addMenu(QtGui.QIcon('assets/icon.ico'),"&TEXT")
        file_menu = self.menu_bar.addMenu('&File')
        edit_menu = self.menu_bar.addMenu('&Edit')
        help_menu = self.menu_bar.addMenu('&Help')
        exit_app = self.menu_bar.addAction('Close',self.Exit)
        
        file_menu.addAction('New', lambda: Purchase.RetailerPurchase())
        file_menu.addAction('Open Saved Bills', lambda: self.SavedBills())
        
        help_ = QAction("Help Center", self)
        help_.triggered.connect(self.HelpCenter)
        help_menu.addAction(help_)

        supp_ = QAction("New Supplier", self)
        supp_.triggered.connect(self.SupplierWindow)
        file_menu.addAction(supp_)
        
    def HelpCenter(self):
        self.customerCare = CustomerCare.Care()
        self.customerCare.show()
        
    def SupplierWindow(self):
        self.supplier = Supplier.SupplierWindow()
        self.supplier.show()
    
    def SavedBills(self):
        dirName = QFileDialog.getExistingDirectory(self, "C:/ProgramData/Invdentory/Billing_Saved_Data")
        
    def Exit(self):
        warning = QMessageBox.warning(self , 'Exit' , "You want to exit?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            sys.exit(MainWindow)
    
    def TabWindow(self):
        # self.quoteWindow = QuoteWindow() 
        barMenu = QtWidgets.QTabWidget(self)
        barMenu.setStyleSheet("""
            QTabBar::tab:selected {background: #1F5B29;}
            QTabBar::tab:selected {color: white;}
            QTabBar::tab {height: 30px; width: 120px; color: white; background: #1F1B24; font-size: 12px;}
            QTabWidget>QWidget> {background: #1F1B24; color: white;}
            QTabWidget::pane {border: 0; color: white;}
        """)
        
        barMenu.addTab(Dashboard.AdminDashboard(), "Dashboard")
        # barMenu.tabBarClicked.connect()
        barMenu.addTab(Sales.CustomerSales(), "Salse")
        barMenu.addTab(Purchase.RetailerPurchase(), "Purchase")
        barMenu.addTab(Return_Product.ReturnProduct(), "Return Purchase")
        self.setCentralWidget(barMenu)
        