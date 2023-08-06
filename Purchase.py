from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
import sqlite3
import datetime
import qrcode
from PIL import Image, ImageDraw, ImageFont

pi,_ = loadUiType('Widgets\Purchase_window.ui')
class RetailerPurchase(QWidget,pi):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.initUI()
        self.buttonHandel()
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
        self.row = self.tableWidget.currentRow
        self.column = self.tableWidget.currentColumn
        self.dt = datetime.datetime.now()
        self.lineEdit_19.setText("%s/%s/%s" % (self.dt.day, self.dt.month, self.dt.year))
        self.lineEdit_13.setText("0")
        self.lineEdit_9.setText("0")
        self.lineEdit_22.setText("0")
        self.checkBox.setChecked(True)
        self.setButtonsStatus(True)
        self.autoCompleter()
        self.autoCompleterVendor()
        self.add_vendors_select_box()
        QLE_On = self.checkBox
        QLE_On.stateChanged.connect(self.Check_Answer)
        
    def autoCompleter(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        self.cur.execute("SELECT Product_Name, Payment_Mode FROM add_products")
        data = self.cur.fetchall()                                         
        self.product_name = []
        self.payment_modes = []
        
        for pro in data:
            pro_name = pro[0]
            pay_mode = pro[1]
            self.product_name.append(pro_name)
            self.payment_modes.append(pay_mode)
            
        product_name_completer = QCompleter(self.product_name)
        pyment_mode_completer = QCompleter(self.payment_modes)
        
        self.lineEdit_4.setCompleter(product_name_completer)
        self.lineEdit_20.setCompleter(pyment_mode_completer)
        
    def autoCompleterVendor(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        self.cur.execute("SELECT vendor_address FROM supplier_details")
        data = self.cur.fetchall() 
        self.vendor_address = []
        
        for pro in data:
            ven_address = pro[0]
            self.vendor_address.append(ven_address)
            
        vendor_address_completer = QCompleter(self.vendor_address)
        self.lineEdit_25.setCompleter(vendor_address_completer)
           
    def Check_Answer(self, state):
        if state == QtCore.Qt.Checked:
            warning = QMessageBox.warning(self , 'Enabled Edit Option' , "Are you sure! Want to edit data" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                self.setEnabledFileds()
                self.setButtonsStatus(True)    
        else:
            self.setDisableFileds() 
            self.setButtonsStatus(True)
                 
        
    def buttonHandel(self):
        self.pushButton_16.clicked.connect(self.add_product)
        self.pushButton_18.clicked.connect(self.delete_product)
        self.pushButton_19.clicked.connect(self.update_product)
        self.pushButton_17.clicked.connect(self.clear)
        self.tableWidget.cellClicked.connect(self.cell_was_clicked)
        self.lineEdit_9.textChanged.connect(self.evaluate_stock_amount)
        self.lineEdit_22.textChanged.connect(self.evaluate_due_amount)
        pass
    
    def add_vendors_select_box(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        self.cur.execute("""SELECT vendor_name	FROM supplier_details""")
        data = self.cur.fetchall()
        for sup in data:
            self.comboBox.addItem(sup[0])
        self.db.close()
    
    def cell_was_clicked(self, row, column):
        current_row = row
        current_column = column
        try:
            cell_value = self.tableWidget.item(current_row, current_column).text()
            self.search(cell_value)
            self.setDisableFileds()
            self.setButtonsStatus(False)
            self.checkBox.setChecked(False)
            
        except:
            print("")
    
    def setButtonsStatus(self, status):
        self.pushButton_16.setEnabled(status)    
        self.pushButton_18.setEnabled(status)      
        self.pushButton_19.setEnabled(status)    
            
    def setDisableFileds(self):
        self.lineEdit_4.setDisabled(1)
        self.lineEdit_7.setDisabled(1)
        self.lineEdit.setDisabled(1)
        self.lineEdit_2.setDisabled(1)
        self.lineEdit_19.setDisabled(1)
        self.lineEdit_13.setDisabled(1)
        self.lineEdit_20.setDisabled(1)
        self.lineEdit_18.setDisabled(1)
        self.comboBox.setDisabled(1)
        self.lineEdit_25.setDisabled(1)
        self.lineEdit_21.setDisabled(1)
        self.lineEdit_22.setDisabled(1)
        self.lineEdit_23.setDisabled(1)
        self.lineEdit_9.setDisabled(1)
        self.lineEdit_8.setDisabled(1)
        self.lineEdit_12.setDisabled(1)
        self.lineEdit_10.setDisabled(1)
        self.lineEdit_17.setDisabled(1)
        self.lineEdit_15.setDisabled(1)
        self.lineEdit_14.setDisabled(1)
        self.lineEdit_16.setDisabled(1)
        
        
    def setEnabledFileds(self):
        self.lineEdit_4.setEnabled(1)
        self.lineEdit.setEnabled(1)
        self.lineEdit_2.setEnabled(1)
        self.lineEdit_13.setEnabled(1)
        self.lineEdit_20.setEnabled(1)
        self.lineEdit_18.setEnabled(1)
        self.comboBox.setEnabled(1)
        self.lineEdit_25.setEnabled(1)
        self.lineEdit_22.setEnabled(1)
        self.lineEdit_9.setEnabled(1)
        self.lineEdit_8.setEnabled(1)
        self.lineEdit_12.setEnabled(1)
        self.lineEdit_10.setEnabled(1)
        self.lineEdit_17.setEnabled(1)
        self.lineEdit_15.setEnabled(1)
        self.lineEdit_14.setEnabled(1)
        self.lineEdit_16.setEnabled(1)
        
        
    def initUI(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.cur.execute("SELECT Product_Name,Product_Code,Purchase_Bill,Supp_Bill,Date,Qty,Payment_Mode,Storage,Supllier_Name,City,Total,Paid,Pay,MRP,Sale_Rate,Discont,Rate,Net_Amount,IGST,Debit_Note,Credit_Note FROM add_products")
        data = self.cur.fetchall()

        self.tableWidget.setRowCount(0)
        self.tableWidget.insertRow(0)

        for row, form in enumerate(data):
            for column, items in enumerate(form):
                self.tableWidget.setItem(row, column, QTableWidgetItem(str(items)))

            rowPosition = self.tableWidget.rowCount()
            self.tableWidget.insertRow(rowPosition)

        self.db.close()
    
    
    def search(self, product_code):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

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
                # self.lineEdit_24.setText(data[8])
                self.comboBox.setCurrentText(data[8])
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
                self.total_balance()
                self.evaluate_stock_amount()
                

            except:
                buttonReply = QMessageBox.information(self,"Sorry","No such Product Code in our Product List. Please try again.")

    def clear(self):
        self.lineEdit_4.setText("")
        self.lineEdit_7.setText("")
        self.lineEdit.setText("")
        self.lineEdit_2.setText("")
        self.lineEdit_13.setText("0")
        self.lineEdit_20.setText("")
        self.lineEdit_18.setText("")
        self.comboBox.setCurrentIndex(0)
        self.lineEdit_25.setText("")
        self.lineEdit_21.setText("0")
        self.lineEdit_22.setText("0")
        self.lineEdit_23.setText("")
        self.lineEdit_9.setText("0")
        self.lineEdit_8.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_10.setText("")
        self.lineEdit_17.setText("")
        self.lineEdit_15.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_16.setText("")
        self.label_23.setText("")
        self.lineEdit_19.setText("%s/%s/%s" % (self.dt.day, self.dt.month, self.dt.year))
        
        self.setButtonsStatus(True)
        self.setEnabledFileds()
        self.lineEdit_7.setEnabled(1)
        self.checkBox.setChecked(False)
    
    def total_balance(self):
        Quantity = int(self.lineEdit_13.text())
        product_price = int(self.lineEdit_9.text())

        self.label_23.setText(str(Quantity*product_price))


    def add_product(self):
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
        Supllier_Name = self.comboBox.currentText()
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
        
                
        
        try:
            data = (Product_Name,Product_Code,Purchase_Bill,Supllier_Bill,Date,Qty,Payment_Mode,Storage,Supllier_Name,
                City,Total,Paid,Pay,MRP,Sale_Rate,Discont,Rate,Net_Amount,IGST,Debit_Note,Credit_Note)
            sql = ''' INSERT INTO add_products VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '''
            self.cur.execute(sql,data)
            self.db.commit()
            self.Qr_Generator()
            self.db.close()
            self.initUI()
        except Exception as e:
            buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}")
    
    def Qr_Generator(self):
        product_code = self.lineEdit_7.text()
        product_name = self.lineEdit_4.text()
        
        fontFile = 'fonts/FreeMono.ttf'
        QRCodefile = (f"QR_Data\{product_name}-{product_code}.png")
        qrObject = qrcode.QRCode(border=3)

        qrObject.add_data(product_code)
        
        qrObject.make()
        image = qrObject.make_image()
        qrLabel = product_code
        draw = ImageDraw.Draw(image)
        QRwidth, QRheight = image.size
        fontSize = 1 #starting font size
        img_fraction = 0.90 # portion of image width you want text width to be, I've had good luck with .90
        fontHeightMax = qrObject.border * qrObject.box_size - 10
        captionX = 0
        captionY = 0
        font = ImageFont.truetype(fontFile, fontSize)
        while font.getsize(qrLabel)[0] < img_fraction*QRwidth and font.getsize(qrLabel)[1] < fontHeightMax:
            fontSize += 1
            font = ImageFont.truetype(fontFile, fontSize)
        captionX = int(QRwidth - font.getsize(qrLabel)[0]) / 2
        draw.text((captionX, captionY), qrLabel, font=font)
        image.save(QRCodefile)
        
                
    def evaluate_stock_amount(self):
        try:
            MRP = int(self.lineEdit_9.text())
            Qty = int(self.lineEdit_13.text())
            total = (MRP*Qty)
            self.lineEdit_21.setText(str(total))
        except Exception as e:
            print(e)
            
    def evaluate_due_amount(self):
        try:
            Total = int(self.lineEdit_21.text())
            Paid = int(self.lineEdit_22.text())
            Pay = (Total-Paid)
            self.lineEdit_23.setText(str(Pay))
        except Exception as e:
            print(e)
            
    def delete_product(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Product_code = self.lineEdit_7.text()
        if Product_code == "":
            buttonreplay = QMessageBox.information(self,"Empty!","Please enter the Product Code ")
        else:
            warning = QMessageBox.warning(self , 'Delete Product' , "Are you sure! Wants to delete this Product?" , QMessageBox.Yes | QMessageBox.No)
            if warning == QMessageBox.Yes :
                sql = ''' DELETE FROM add_products WHERE Product_code = ? '''
                self.cur.execute(sql , [(Product_code)])
                self.db.commit()
                self.initUI()    
        
     
    def update_product(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        self.Product_Name = self.lineEdit_4.text()
        self.Product_Code = self.lineEdit_7.text()
        self.Purchase_Bill = self.lineEdit.text()
        self.Supllier_Bill = self.lineEdit_2.text()
        self.Date = self.lineEdit_19.text()
        self.Qty = self.lineEdit_13.text()
        self.Payment_Mode = self.lineEdit_20.text()
        self.Storage = self.lineEdit_18.text()
        self.Supllier_Name = self.comboBox.currentText()
        self.City = self.lineEdit_25.text()
        self.Total = self.lineEdit_21.text()
        self.Paid = self.lineEdit_22.text()
        self.Pay = self.lineEdit_23.text()
        self.MRP = self.lineEdit_9.text()
        self.Sale_Rate = self.lineEdit_8.text()
        self.Discont = self.lineEdit_12.text()
        self.Rate = self.lineEdit_10.text()
        self.Net_Amount = self.lineEdit_17.text()
        self.IGST = self.lineEdit_15.text()
        self.Debit_Note = self.lineEdit_14.text()
        self.Credit_Note = self.lineEdit_16.text()

        if self.Product_Code == "":
            dfdsfsd = QMessageBox.information(self,"Alert!","Please enter product details.")
        else:
            try:
                self.cur.execute(f""" UPDATE add_products SET 
                            Product_Name = '{self.Product_Name}',
                            Purchase_Bill = '{self.Purchase_Bill}',
                            Supp_Bill = '{self.Supllier_Bill}',
                            Date = '{self.Date}',
                            Qty = '{self.Qty}',
                            Payment_Mode = '{self.Payment_Mode}',
                            Storage = '{self.Storage}',
                            Supllier_Name = '{self.Supllier_Name}',
                            City = '{self.City}',
                            Total = '{self.Total}',
                            Paid = '{self.Paid}',
                            Pay = '{self.Pay}',
                            MRP = '{self.MRP}',
                            Sale_Rate = '{self.Sale_Rate}',
                            Discont = '{self.Discont}',
                            Rate = '{self.Rate}',
                            Net_Amount = '{self.Net_Amount}',
                            IGST = '{self.IGST}',
                            Debit_Note = '{self.Debit_Note}',
                            Credit_Note = '{self.Credit_Note}' 
                            WHERE Product_Code = '{self.Product_Code}' """)
                self.db.commit()
                self.initUI()
                self.db.close()
                dfdsfsd = QMessageBox.information(self,"Updated","Product Successfully Updated.")
            except Exception as e:
                dfdsfsd = QMessageBox.information(self,"Failed!",f"{e}")
            
                     