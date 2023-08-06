from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import Purchase

ri,_ = loadUiType('Widgets\_return_propduct_window.ui')
class ReturnProduct(QWidget,ri):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.buttonHandel()
        self.initUI()
        self.lineEdit_26.setText("0")
        self.tableWidget.verticalHeader().setVisible(False)
        self.autoCompleter()
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
                QTableWidget::item { color: white; font: 9pt "Segoe UI"; }   
            """)
        
        
    def buttonHandel(self):
        self.pushButton_16.clicked.connect(self.return_product)
        self.pushButton_17.clicked.connect(self.clear)
        self.lineEdit_7.textChanged.connect(self.search)
        
        pass
    
    def initUI(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Product_Name,Product_Code,Purchase_Bill,Supp_Bill,Date,Qty,Payment_Mode,Storage,Supllier_Name,City,Total,Paid,Pay,MRP,Sale_Rate,Discont,Rate,Net_Amount,IGST,Debit_Note,Credit_Note FROM return_products")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

        self.db.close()
    
    def autoCompleter(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        self.cur.execute("SELECT Product_Code FROM add_products")
        data = self.cur.fetchall()                                         
        self.product_code= []
        
        for pro in data:
            pro_code = pro[0]
            self.product_code.append(pro_code)
            
        product_code_completer = QCompleter(self.product_code)
        self.lineEdit_7.setCompleter(product_code_completer)
        
        
    def return_product(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        Product_Name = self.lineEdit_4.text()
        Product_Code = self.lineEdit_7.text()
        Purchase_Bill = self.lineEdit.text()
        Supllier_Bill = self.lineEdit_2.text()
        Date = self.lineEdit_19.text()
        Qty = self.lineEdit_13.text()
        Payment_Mode = self.lineEdit_20.text()
        Storage = self.lineEdit_18.text()
        Supllier_Name = self.lineEdit_24.text()
        City = self.lineEdit_25.text()
        Total = self.lineEdit_21.text()
        Paid = self.lineEdit_22.text()
        Pay = self.lineEdit_23.text()
        MRP = self.lineEdit_9.text()
        Sale_Rate = self.lineEdit_8.text()
        Discont = self.lineEdit_12.text()
        Rate = self.lineEdit_10.text()
        Net_Amount = self.lineEdit_17.text()
        IGST = self.lineEdit_15.text()
        Debit_Note = self.lineEdit_14.text()
        Credit_Note = self.lineEdit_16.text()
        return_qty = self.lineEdit_26.text()
        
        if Product_Code == "":
            bb = QMessageBox.information(self , 'Return Product!' , "Please enter product code. (All product information is required!))" , QMessageBox.Yes)
        elif return_qty == "0" :
            bb = QMessageBox.information(self , 'Return Product!' , "You have entered zero(0) Product Qty! (Quantity cannot be zero(0))" , QMessageBox.Yes)
        elif return_qty == "":
            bb = QMessageBox.information(self , 'Return Product!' , "Product Qty cannot be blank!" , QMessageBox.Yes)
        else:   
            warning = QMessageBox.warning(self , 'Return Product!' , "Are you sure! Wants to Return this Product?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes:
                try:
                    data = (Product_Name,Product_Code,Purchase_Bill,Supllier_Bill,Date,return_qty,Payment_Mode,Storage,Supllier_Name,
                        City,Total,Paid,Pay,MRP,Sale_Rate,Discont,Rate,Net_Amount,IGST,Debit_Note,Credit_Note)
                    sql = ''' INSERT INTO return_products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
                    self.cur.execute(sql,data)
                    self.db.commit()
                    self.update_quantity()
                    self.db.close()
                    self.search()
                    if Qty == return_qty:
                        self.db = sqlite3.connect('DB\db.db')
                        self.cur = self.db.cursor()
                        Product_code = self.lineEdit_7.text()
                        sql = ''' DELETE FROM add_products WHERE Product_code = ? '''
                        self.cur.execute(sql , [(Product_code)])
                        self.db.commit()
                        self.initUI() 
                    self.initUI()
                except Exception as e:
                    buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}")

                
    def search(self):
        self.lineEdit_26.setText("0")
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        product_code = self.lineEdit_7.text()

        if product_code == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Artical Number")
        else: 
            sql = ''' SELECT * FROM add_products WHERE Product_Code = ? '''
            self.cur.execute(sql , [(product_code)])
            
            data = self.cur.fetchone()

            try:   
                self.lineEdit_4.setText(data[0])
                self.lineEdit_7.setText(data[1])
                self.lineEdit.setText(data[2])
                self.lineEdit_2.setText(data[3])
                self.lineEdit_19.setText(data[4])
                self.lineEdit_13.setText(data[5])
                self.lineEdit_20.setText(data[6])
                self.lineEdit_18.setText(data[7])
                self.lineEdit_24.setText(data[8])
                self.lineEdit_25.setText(data[9])
                self.lineEdit_21.setText(data[10])
                self.lineEdit_22.setText(data[11])
                self.lineEdit_23.setText(data[12])
                self.lineEdit_9.setText(data[13])
                self.lineEdit_8.setText(data[14])
                self.lineEdit_12.setText(data[15])
                self.lineEdit_10.setText(data[16])
                self.lineEdit_17.setText(data[17])
                self.lineEdit_15.setText(data[18])
                self.lineEdit_14.setText(data[19])
                self.lineEdit_16.setText(data[20])
                self.initUI()  
            
            except:
               print("No product code found")
               
               
    def update_quantity(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        Product_Code = self.lineEdit_7.text()
        return_qty = self.lineEdit_26.text()
        
        try:
            self.cur.execute(f"UPDATE add_products  SET Qty = Qty-'{return_qty}' WHERE Product_Code = '{Product_Code}' ")
            self.db.commit()
            self.db.close()
        except:
            sasd = QMessageBox.information(self,"Information","Please add products before generate bill")

    def clear(self):
        
        pass