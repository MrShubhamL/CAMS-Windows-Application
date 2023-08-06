from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3
from tkinter import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUiType
import datetime

si,_ = loadUiType('Widgets/Supplier_window.ui')
class SupplierWindow(QMainWindow,si):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Customer Care")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setupUi(self)
        self.show()
        self.initUI()
        self.dt = datetime.datetime.now()
        self.lineEdit_3.setText("%s/%s/%s" % (self.dt.day, self.dt.month, self.dt.year))
        self.handelButtons()
        self.tableWidget.verticalHeader().setVisible(False)
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
        
    def handelButtons(self):
        self.pushButton_9.clicked.connect(self.add_vendor)
        self.pushButton_11.clicked.connect(self.update_vendor)
        self.pushButton_12.clicked.connect(self.delete_vendor)
        self.pushButton_10.clicked.connect(self.clear)
        self.close_button_2.clicked.connect(self.Exit)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.lineEdit_7.textChanged.connect(self.create_vendor_code)
        
    def cell_was_clicked(self, row, column):
        current_row = row
        current_column = column
        try:
            cell_value = self.tableWidget.item(current_row, current_column).text()
            self.search(cell_value)
        except:
            print("")

    def search(self, vendor_code):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        if vendor_code == "":
            buttonReply = QMessageBox.information(self,"Empty","Please Enter The Artical Number")
        else: 
            sql = ''' SELECT * FROM supplier_details WHERE vendor_code = ? '''
            self.cur.execute(sql , [(vendor_code)])
            
            data = self.cur.fetchone()

            try:   
                self.lineEdit_6.setText(data[0])
                self.lineEdit_4.setText(data[1])
                self.lineEdit_5.setText(data[2])
                self.lineEdit_7.setText(data[3])
                self.lineEdit_15.setText(data[4])
                
                self.lineEdit_8.setText(data[5])
                self.lineEdit_9.setText(data[6])
                self.lineEdit_10.setText(data[7])
                self.lineEdit_11.setText(data[8])
                
                self.lineEdit_12.setText(data[9])
                self.lineEdit_13.setText(data[10])
                self.lineEdit_14.setText(data[11])
                self.initUI()  
            except:
                buttonReply = QMessageBox.information(self,"Sorry","No such Vender Code in our Supplier List. Please try again.")
      
        
    def initUI(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        self.cur.execute("""SELECT 
                            vendor_code,
                            company_name,	
                            address,	
                            phone_no,	
                            website,	
                            product_details,	
                            service_details,	
                            license_no,	
                            gst_no,	
                            vendor_name,	
                            vendor_contact,	
                            vendor_address FROM supplier_details""")
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)
        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))
            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)
        self.db.close()
        
    def create_vendor_code(self):
        company_phone = self.lineEdit_7.text()
        v_code = "VEND"+company_phone
        self.lineEdit_6.setText(str(v_code))
        if company_phone == "":
            self.lineEdit_6.setText("")
            
        
    def add_vendor(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        
        company_name = self.lineEdit_4.text()
        company_address = self.lineEdit_5.text()
        company_phone = self.lineEdit_7.text()
        company_website = self.lineEdit_15.text()
        
        product_details = self.lineEdit_8.text()
        service_details = self.lineEdit_9.text()
        lincese_number = self.lineEdit_10.text()
        gst_number = self.lineEdit_11.text()
        
        vendor_name = self.lineEdit_12.text()
        vendor_contact = self.lineEdit_13.text()
        vendor_address = self.lineEdit_14.text()
        vendor_code = self.lineEdit_6.text()
        
        if vendor_code == "":
            mm = QMessageBox.information(self, "Invalid!", "Please enter the vendor code | All fileds required!")
        else:
            try:
                data = (
                    vendor_code,
                    company_name,
                    company_address,
                    company_phone,
                    company_website,
                    product_details,
                    service_details,
                    lincese_number,
                    gst_number,
                    vendor_name,
                    vendor_contact,
                    vendor_address
                )
                
                sql = ''' INSERT INTO supplier_details VALUES (?,?,?,?,?,?,?,?,?,?,?,?) '''
                self.cur.execute(sql,data)
                self.db.commit()
                self.db.close()
                self.initUI()
                self.clear()
            except Exception as e:
                buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}")
    
    def update_vendor(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        company_name = self.lineEdit_4.text()
        company_address = self.lineEdit_5.text()
        company_phone = self.lineEdit_7.text()
        company_website = self.lineEdit_15.text()
        
        product_details = self.lineEdit_8.text()
        service_details = self.lineEdit_9.text()
        lincese_number = self.lineEdit_10.text()
        gst_number = self.lineEdit_11.text()
        
        vendor_name = self.lineEdit_12.text()
        vendor_contact = self.lineEdit_13.text()
        vendor_address = self.lineEdit_14.text()
        vendor_code = self.lineEdit_6.text()
        
        
        try:
            self.cur.execute(f""" UPDATE supplier_details SET 
                company_name = '{company_name}',
                address = '{company_address}',
                phone_no = '{company_phone}',
                website = '{company_website}',
                product_details = '{product_details}',
                service_details = '{service_details}',
                license_no = '{lincese_number}',
                gst_no = '{gst_number}',
                vendor_name = '{vendor_name}',
                vendor_contact = '{vendor_contact}',
                vendor_address = '{vendor_address}'
                WHERE vendor_code = '{vendor_code}'""")
            self.db.commit()
            self.initUI()
            self.db.close()
            dfdsfsd = QMessageBox.information(self,"Updated","Vendor Details Successfully Updated.")
        except Exception as e:
            buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}") 
    
    def delete_vendor(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        vendor_code = self.lineEdit_6.text()
        if vendor_code == "":
            buttonreplay = QMessageBox.information(self,"Empty!","Please enter the Vendor Code ")
        else:
            warning = QMessageBox.warning(self , 'Delete Vendor' , "Are you sure! Wants to delete this Vendor?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                sql = ''' DELETE FROM supplier_details WHERE vendor_code = ? '''
                self.cur.execute(sql , [(vendor_code)])
                self.db.commit()
                self.initUI()    
        
        
    def clear(self):
        self.lineEdit_4.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_6.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit_15.setText("")
        
        self.lineEdit_8.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_11.setText("")
        
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
          
        
    def Exit(self):
        self.close()
        
 
