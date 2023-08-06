
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from tkinter import*
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QPen, QBrush

di,_ = loadUiType('Widgets\Dashboard_window.ui')
class AdminDashboard(QWidget,di):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.initUI()
        self.initUI2()
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.setStyleSheet("""
              QHeaderView::section {
                    background-color: #646464;
                    border-style: none;
                    border-bottom: 1px solid #fffff8;
                    border-right: 1px solid #fffff8;
                    color: white;
                }

                QHeaderView::section:horizontal
                {
                    border-top: 1px solid #fffff8;
                }

                QHeaderView::section:vertical
                {
                    border-left: 1px solid #fffff8;
                }         
                QTableWidget::item { color: white; font: 9pt "Segoe UI"; padding-left: 10px;}   
            """)
        self.tableWidget.cellClicked.connect(self.initUI)
        self.tableWidget_2.cellClicked.connect(self.initUI2)


        
    def initUI(self):
        self.cal_toatl_stock_amt()
        self.cal_toatl_stock_qty()
        self.cal_toatl_return_stock_amt()
        self.cal_toatl_return_stock_qty()
        self.cal_toatl_profite_amt()
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT customer_name,customer_email,customer_contact,customer_address,total_purchase,purchase_bill_no,purchase_date FROM customer_purchase")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

        self.db.close()

        
    def initUI2(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Product_Name,Product_Code,Date,Qty,Sale_Rate FROM add_products")
        data = self.cur.fetchall()

        self.tableWidget_2.setRowCount(0)
        self.tableWidget_2.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget_2.rowCount()
            self.tableWidget_2.insertRow(rowPosition)

        self.db.close()
        
        
    def cal_toatl_stock_amt(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT MRP FROM add_products")
        data = self.cur.fetchall()
        total_amt = 0
        for amt in data:
            total_amt += int(amt[0])
        self.label_3.setText("  "+str(total_amt))
        self.db.close()
        
    def cal_toatl_stock_qty(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Qty FROM add_products")
        data = self.cur.fetchall()
        total_qty = 0
        for qty in data:
            total_qty += int(qty[0])
        self.label_7.setText("     "+str(total_qty))
        self.db.close()
        
    def cal_toatl_return_stock_amt(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT MRP FROM return_products")
        data = self.cur.fetchall()
        total_amt = 0
        for amt in data:
            total_amt += int(amt[0])
        self.label_25.setText("  "+str(total_amt))
        self.db.close()
        
    def cal_toatl_return_stock_qty(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Qty FROM return_products")
        data = self.cur.fetchall()
        total_qty = 0
        for qty in data:
            total_qty += int(qty[0])
        self.label_27.setText("       "+str(total_qty))
        self.db.close()
        
                
    def cal_toatl_profite_amt(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT total_purchase FROM customer_purchase")
        data = self.cur.fetchall()
        total_prof = 0
        for prof in data:
            total_prof += float(prof[0])
        self.label_29.setText("  "+str(total_prof))
        self.db.close()
        