
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sqlite3
from tkinter import*
from PyQt5.uic import loadUiType
from PyQt5.QtCore import Qt
from PyQt5.QtCore import Qt
import datetime
from docxtpl import DocxTemplate
import os
import random
import calendar
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
import  os
import cv2
import time

ui,_ = loadUiType('Widgets\Sales_window.ui')
class CustomerSales(QWidget,ui):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales")
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setGeometry(0,0,1366,768)
        self.setupUi(self)
        self.buttonHandel()
        self.l = []
        self.invoice_list = [[]]
        self.setStyleSheet("""
            QMessageBox{background-color: white; color: black;}
            """)
        self.z1.setText("0")
        self.z2.setText("0")
        self.z3.setText("0")
        self.z4.setText("0")
        self.z5.setText("0")
        self.z6.setText("0")
        
        self.g1.setText("0")
        self.g2.setText("0")
        self.g3.setText("0")
        self.g4.setText("0")
        self.g5.setText("0")
        self.g6.setText("0")
        
        self.x1.setText("0")
        self.x2.setText("0")
        self.x3.setText("0")
        self.x4.setText("0")
        self.x5.setText("0")
        self.x6.setText("0")
        
        self.y1.setText("0")
        self.y2.setText("0")
        self.y3.setText("0")
        self.y4.setText("0")
        self.y5.setText("0")
        self.y6.setText("0")
        
        self.lineEdit_14.setText("0")
        self.dt = datetime.datetime.now()
        self.current_date1 = str("%s %s %s" % (self.dt.day, self.dt.month, self.dt.year))
        self.current_date2 = str("%s/%s/%s" % (self.dt.day, self.dt.month, self.dt.year))
        self.label_31.setText(str(self.current_date2))
        self.findDay()    
        self.docGSTInvoice = DocxTemplate("templates/gst_invoice_template.docx")
        self.docInvoice = DocxTemplate("templates/invoice_template.docx")
        self.Bill_Number = 0
        self.autoCompleter()
        self.lineEdit_5.setText("0.0")
        self.lineEdit_7.setText("0.0")
        
        QLE_On = self.checkBox
        QLE_On.stateChanged.connect(self.Check_Answer)
     
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
        self.lineEdit_4.setCompleter(product_code_completer)
        
    def findDay(self):
        born = datetime.datetime.strptime(self.current_date1, '%d %m %Y').weekday() 
        todayDate = calendar.day_name[born] 
        self.label_11.setText(str(todayDate))
    
    def Check_Answer(self, state):
        pro_gst = self.gst_line_2.text()
        if state == QtCore.Qt.Checked:
            self.zeroGST()    
        else:
            self.gst_line.setText(pro_gst)
              
    def zeroGST(self):
        self.gst_line.setText("0")
        pass
    
    
    def buttonHandel(self):
        self.pushButton_9.clicked.connect(self.add_bill)
        self.pushButton_21.clicked.connect(self.Hiding_Themes)
        self.pushButton_14.clicked.connect(self.Handel_UI_Changes)
        self.lineEdit_4.textChanged.connect(self.search)
        self.lineEdit_7.textChanged.connect(self.net_amount_cal)
        self.pushButton_11.clicked.connect(self.Generate)
        self.pushButton_12.clicked.connect(self.clear)
        self.pushButton_15.clicked.connect(self.printGSTInvoice)
        self.pushButton_16.clicked.connect(self.printInvoice)
        self.pushButton_17.clicked.connect(self.add_QR_data)
        
        
        
        pass
    

    def Handel_UI_Changes(self):
        self.Hiding_Themes()
        self.groupBox_4.setVisible(True)

        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()

        total = self.lineEdit_17.text()
        total_gst = self.lineEdit_14.text()
        
        product_name1 = self.a1.text()
        product_name2 = self.a2.text()
        product_name3 = self.a3.text()
        product_name4 = self.a4.text()
        product_name5 = self.a5.text()
        product_name6 = self.a6.text()


        MRP1 = self.x1.text()
        MRP2= self.x2.text()
        MRP3= self.x3.text()
        MRP4= self.x4.text()
        MRP5= self.x5.text()
        MRP6= self.x6.text()



        QTY1 = self.y1.text()
        QTY2 = self.y2.text()
        QTY3 = self.y3.text()
        QTY4 = self.y4.text()
        QTY5 = self.y5.text()
        QTY6 = self.y6.text()


        IGST1 = self.g1.text()
        IGST2 = self.g2.text()
        IGST3 = self.g3.text()
        IGST4 = self.g4.text()
        IGST5 = self.g5.text()
        IGST6 = self.g6.text()
        


        Total1 = self.z1.text()
        Total2 = self.z2.text()
        Total3 = self.z3.text()
        Total4 = self.z4.text()
        Total5 = self.z5.text()
        Total6 = self.z6.text()

       
        # current = ("%s:%s:%s" % dt.day,dt.month,dt.year)
        
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        
  
        

        # self.textEdit.delete(1.0,END)
        self.textEdit.insertPlainText(str(f"\n                                              HARIOM ENTERPRISES              "))   
        self.textEdit.insertPlainText(str(f"\n                                             SALES, SERVIECS & AMC         "))
        self.textEdit.insertPlainText(str(f"\n	                 Tejas Sutar - 7875454612\n"))
        self.textEdit.insertPlainText("--------------------------------------------------------------------------------------")
        self.textEdit.insertPlainText(str("\n                             Computer Peripherals | PC Accessories\n Buy Cables, Connectors, Add On Cards, USB Hubs, Headphones, Game Pads,\n Cooling Pads at Best Prices. shop Now!         \n\n"))
        self.textEdit.insertPlainText(str("Address - 22/584 Hariom Industries, Ganesh nagar, 2nd Lane, Ichalkaranji 416115           \n"))
        self.textEdit.insertPlainText("--------------------------------------------------------------------------------------")
        self.textEdit.insertPlainText(f"\n Bill Number:  {str(self.Bill_Number)}")
        self.textEdit.insertPlainText(f"\n Customer Name:  {customer_Name}")
        self.textEdit.insertPlainText(f"\n Phone Number:  {contact_number}")
        self.textEdit.insertPlainText(f"\n Customer Email:  {customer_Email}")
        self.textEdit.insertPlainText(f"\n Date:  {self.current_date1}")
        self.textEdit.insertPlainText("\n --------------------------------------------------------------------------------------")
        self.textEdit.insertPlainText(f"\n Sr.No.    Product Name\tRate\tQty\tIGST\tTotal")
        self.textEdit.insertPlainText("\n --------------------------------------------------------------------------------------")
        self.textEdit.insertPlainText(f"\n 1.                {product_name1}\t{MRP1}\t{QTY1}\t{IGST1}         \t{Total1}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText(f"\n 2.                {product_name2}\t{MRP2}\t{QTY2}\t{IGST2}         \t{Total2}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText(f"\n 3.                {product_name3}\t{MRP3}\t{QTY3}\t{IGST3}         \t{Total3}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText(f"\n 4.                {product_name4}\t{MRP4}\t{QTY4}\t{IGST4}         \t{Total4}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText(f"\n 5.                {product_name5}\t{MRP5}\t{QTY5}\t{IGST5}         \t{Total5}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText(f"\n 6.                {product_name6}\t{MRP6}\t{QTY6}\t{IGST6}         \t{Total6}")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText("\n")
        self.textEdit.insertPlainText("\n --------------------------------------------------------------------------------------")
        self.textEdit.insertPlainText(f"\n                                                                                                    Total IGST:       {total_gst}")
        self.textEdit.insertPlainText(f"\n                                                                                                    Total Amount: {total}")
        self.textEdit.insertPlainText(str("\n Tearms & Conditions:"))
        self.textEdit.insertPlainText(str("\n No Return No Exchange"))
        self.textEdit.insertPlainText(str("\n No Guarantee No Warranty"))

            
            
    def Hiding_Themes(self):
        self.groupBox_4.hide()
        self.textEdit.setText("")            
    
    def net_amount_cal(self):
        try:
            sale_rate = self.lineEdit_5.text()
            discount = self.lineEdit_7.text()
            net_amount = (float(sale_rate) - float(discount))
            self.lineEdit_9.setText(str(net_amount))
        except Exception as e:
            print(f"{e}")
         
    
    def add_QR_data(self):
       
        try:
            cap = cv2.VideoCapture(0)
            cap.set(3, 800)
            cap.set(4, 400)
            # initialize the OpenCV QRCode detector
            detector = cv2.QRCodeDetector()
            while True:
                success, img = cap.read()
                # detect and decode
                data, vertices_array, _ = detector.detectAndDecode(img)
                # check if there is a QRCode in the image
                if vertices_array is not None:
                    if data:
                        self.lineEdit_4.setText(str(data))
                        self.add_bill()
                        break
                # display the result
                cv2.imshow("QR Code Scanner", img)
                # Enter q to Quit
                if cv2.waitKey(1) == ord("q"):
                    break
            cap.release()
            cv2.destroyAllWindows()
        except:
            ButtonReaplay = QMessageBox.information(self,"Camera","Please sure to connect respective device")
        
    def add_bill(self):
        # self.timer=QTimer()
        # self.timer.start(500)
        # self.timer.timeout.connect(self.clear_filed)
        
        self.net_amount_cal()
        self.applied_gst_amount = 0.0
        self.includeGST = 0.0
        self.Hiding_Themes()
        self.Disc = self.lineEdit_7.text()
        self.Qty = self.lineEdit_3.text()
        self.product_n = self.product_name.text()
        self.product_code = self.lineEdit_4.text()
        self.net_Amount = self.lineEdit_9.text()
        self.GST = self.gst_line.text()
        try:
            s1 = float(self.lineEdit_9.text())
            s2 = float(self.lineEdit_3.text())

            self.lineEdit_9.setText(str(s1*s2))
            GSTPercentage = float(self.GST)
            amountWithoutGst = float(s1*s2)
            # self.total = str(self.lineEdit_9.text())
            
            # 1,000+ (1,000X(18/100)) = 1,000+180 = Rs. 1,180
            self.includeGST = amountWithoutGst + ((amountWithoutGst)*((GSTPercentage)/100))
            
            self.applied_gst_amount = float(self.includeGST) - amountWithoutGst
            self.l1 = []
            self.l1.append(str(self.product_n))
            self.l1.append(str(self.product_code))
            self.l1.append(str(self.net_Amount))
            self.l1.append(str(self.Qty))
            self.l1.append(str(self.applied_gst_amount))
            self.l1.append(str("("+self.GST+"%)"))
            self.l1.append(str(self.includeGST))
            self.l1.append(str(amountWithoutGst))
            self.l.append(self.l1)

            for i in range(0,len(self.l)):
                a = 'a' + (str(i+1))
                if a == "a1":
                    self.a1.setText(str(self.l[i][0])) 
                    self.c1.setText(str(self.l[i][1]))
                    self.x1.setText(str(self.l[i][2]))
                    self.y1.setText(str(self.l[i][3]))
                    self.g1.setText(str(self.l[i][4]))
                    self.s1.setText(str(self.l[i][5]))
                    self.z1.setText(str(self.l[i][6]))
                    
                elif a == "a2":
                    self.a2.setText(str(self.l[i][0]))
                    self.c2.setText(str(self.l[i][1])) 
                    self.x2.setText(str(self.l[i][2]))
                    self.y2.setText(str(self.l[i][3]))
                    self.g2.setText(str(self.l[i][4]))
                    self.s2.setText(str(self.l[i][5]))
                    self.z2.setText(str(self.l[i][6]))
                    
                elif a == "a3":
                    self.a3.setText(str(self.l[i][0])) 
                    self.c3.setText(str(self.l[i][1]))
                    self.x3.setText(str(self.l[i][2]))
                    self.y3.setText(str(self.l[i][3]))
                    self.g3.setText(str(self.l[i][4]))
                    self.s3.setText(str(self.l[i][5]))
                    self.z3.setText(str(self.l[i][6]))
                    
                elif a == "a4":
                    self.a4.setText(str(self.l[i][0])) 
                    self.c4.setText(str(self.l[i][1]))
                    self.x4.setText(str(self.l[i][2]))
                    self.y4.setText(str(self.l[i][3]))
                    self.g4.setText(str(self.l[i][4]))
                    self.s4.setText(str(self.l[i][5]))
                    self.z4.setText(str(self.l[i][6]))
                    
                elif a == "a5":
                    self.a5.setText(str(self.l[i][0])) 
                    self.c5.setText(str(self.l[i][1]))
                    self.x5.setText(str(self.l[i][2]))
                    self.y5.setText(str(self.l[i][3]))
                    self.g5.setText(str(self.l[i][4]))
                    self.s5.setText(str(self.l[i][5]))
                    self.z5.setText(str(self.l[i][6]))
                    
                elif a == "a6":
                    self.a6.setText(str(self.l[i][0])) 
                    self.c6.setText(str(self.l[i][1]))
                    self.x6.setText(str(self.l[i][2]))
                    self.y6.setText(str(self.l[i][3]))
                    self.g6.setText(str(self.l[i][4]))
                    self.s6.setText(str(self.l[i][5]))
                    self.z6.setText(str(self.l[i][6]))
                
        except:
            buttdsf = QMessageBox.information(self,"Warning!","Please Enter valid Product Code and Product Qty.")
                
    def clear_filed(self):
        self.product_name.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_3.setText("")
        self.lineEdit_5.setText("")
        self.lineEdit_7.setText("")
        self.gst_line.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_17.setText("")       
        # self.timer.stop()
        pass           
    def search(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        

        Product_Code = self.lineEdit_4.text()
        avalable_stock = self.label_29.text()
        
        if Product_Code == "":
            uttonReply = QMessageBox.information(self,"Empty","Please Enter The Product Code")
        else:
            sql = ''' SELECT * FROM add_products WHERE Product_Code = ? '''
            self.cur.execute(sql , [(Product_Code)])
                
            data = self.cur.fetchone()

            try:   
                self.product_name.setText(data[0])
                self.lineEdit_5.setText(data[14])
                self.lineEdit_7.setText(data[15])
                self.gst_line.setText(data[18])
                self.gst_line_2.setText(data[18])
                self.availabel_Quantity()
                    
        
            except:
                print("Exception")
                # buttonReply = QMessageBox.information(self,"Sorry!","No Such Artical Number In Our Product List Please Check Artical Number")
                # self.statusBar().showMessage("No Such Artical Number In Our Product List Please Check Artical Number")

           
    def availabel_Quantity(self):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()

        Product_Code = self.lineEdit_4.text()

        sql = ''' SELECT * FROM add_products WHERE Product_Code = ? '''
        self.cur.execute(sql , [(Product_Code)])

        data = self.cur.fetchone()

        try:   
            self.label_29.setText(data[5])
        except:
            QMessageBox.information(self,"Sorry!","No Such Artical Number In Our Product List Please Check Artical Number")
          
    def total_update_stock(self):
        product_code = []
        product_qty = []
        for i in self.l:
            pro_code = i[1]
            product_code.append(pro_code)
        
        for j in self.l:
            pro_qty = j[3]
            product_qty.append(pro_qty)
        
        for i,j in zip(product_code,product_qty):
            self.update_quantity(i,j)
    
         
    def update_quantity(self, product_code, qty):
        # self.db = mysql.connector.connect(host='localhost' , user='root' , password ='shubh96S@' , db='data')
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        try:
            self.cur.execute(f"UPDATE add_products  SET Qty = Qty-'{qty}' WHERE Product_Code = '{product_code}' ")
            self.db.commit()
            self.db.close()

        except:
            sasd = QMessageBox.information(self,"Information","Please add products before generate bill")

    def Generate(self):
        self.Bill_Number = random.randint(999,9999999)
        self.welcome()
        self.total_update_stock()
        self.add_customer_purchase()

    def welcome(self):
        
        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()
        if customer_Name =="" and contact_number =="":
            hggh = QMessageBox.information(self,"Alert!","Customer Name & Contact is mendentory")
        else:
            self.lineEdit_13.setText(customer_Name)
            self.lineEdit_18.setText(customer_Email)
            self.lineEdit_19.setText(contact_number)

            a = float(self.z1.text())
            b = float(self.z2.text())
            c = float(self.z3.text())
            d = float(self.z4.text())
            e = float(self.z5.text())
            f = float(self.z6.text())

            g = float(self.g1.text())
            h = float(self.g2.text())
            i = float(self.g3.text())
            j = float(self.g4.text())
            k = float(self.g5.text())
            l = float(self.g6.text())

            self.lineEdit_15.setText(str(a+b+c+d+e+f))
            self.lineEdit_17.setText(str(a+b+c+d+e+f))
            self.lineEdit_14.setText(str(g+h+i+j+k+l))
            


    def printfile(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.accepted:
            self.textEdit.print_(printer)

    def printGSTInvoice(self):
        self.saveGSTInvoice()
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer,self)
        previewDialog.paintRequested.connect(self.printer_priview2)
        previewDialog.exec_()

    def printInvoice(self):
        self.saveInvoice()
        
    
    def printer_priview2(self, printer):
        self.textEdit.print_(printer)
        
            
    def clear(self):
        self.a1.setText("")
        self.x1.setText("")
        self.a2.setText("")
        self.x2.setText("")
        self.a3.setText("")
        self.x3.setText("")
        self.a4.setText("")
        self.x4.setText("")
        self.a5.setText("")
        self.x5.setText("")
        self.a6.setText("")
        self.x6.setText("")
        self.y1.setText("")
        self.z1.setText("0")
        self.y2.setText("")
        self.z2.setText("0")
        self.y3.setText("")
        self.z3.setText("0")
        self.y4.setText("")
        self.z4.setText("0")
        self.y5.setText("")
        self.z5.setText("0")
        self.y6.setText("")
        self.z6.setText("0")
        self.g1.setText("0")
        self.g2.setText("0")
        self.g3.setText("0")
        self.g4.setText("0")
        self.g5.setText("0")
        self.g6.setText("0")
        self.s1.setText("")
        self.s2.setText("")
        self.s3.setText("")
        self.s4.setText("")
        self.s5.setText("")
        self.s6.setText("")
        
        self.c1.setText("")
        self.c2.setText("")
        self.c3.setText("")
        self.c4.setText("")
        self.c5.setText("")
        self.c6.setText("")

        self.product_name.setText("")
        self.lineEdit_4.setText("")
        self.lineEdit_3.setText("")
        
        self.lineEdit_6.setText("")
        self.textEdit_2.setText("")
        self.lineEdit_8.setText("")
        self.lineEdit_12.setText("")
        self.lineEdit_13.setText("")
        self.lineEdit_14.setText("")
        self.lineEdit_15.setText("")
        
        self.lineEdit_5.setText("")
        self.lineEdit_7.setText("")
        self.gst_line.setText("")
        self.lineEdit_9.setText("")
        self.lineEdit_17.setText("")
        
  
        self.lineEdit_18.setText("")
        self.lineEdit_19.setText("")

        self.label_29.setText("")

        # self.lineEdit_20.setText("")

        self.l = []
        self.Hiding_Themes()
      
    def saveGSTInvoice(self):
        self.GSTInvoice()
        warning = QMessageBox.warning(self , 'Save Bill to PDF' , "Do you want to save bill to PDF?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            filePath = "C:/ProgramData/Inventory/Billing_Saved_Data/"+"invoice-"+str(self.Bill_Number)+"("+str(self.current_date1)+").docx"
            if os.path.isfile(filePath):
                os.startfile(filePath, 'print')  
            else:
                warning = QMessageBox.warning(self , 'Alert' , f"{filePath} could not be printed!" , QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes :
                    print("Exception")
      
    def saveInvoice(self):
        self.invoice()
        warning = QMessageBox.warning(self , 'Save Bill to PDF' , "Do you want to save bill to PDF?" , QMessageBox.Yes | QMessageBox.No)
        if warning == QMessageBox.Yes :
            filePath = "C:/ProgramData/Inventory/Billing_Saved_Data/"+"invoice-"+str(self.Bill_Number)+"("+str(self.current_date1)+").docx"
            if os.path.isfile(filePath):
                os.startfile(filePath, 'print')  
            else:
                warning = QMessageBox.warning(self , 'Alert' , f"{filePath} could not be printed!" , QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes :
                    print("Exception")
    

                
                
    def GSTInvoice(self):
        current_date = str("%s:%s:%s" % (self.dt.day, self.dt.month, self.dt.year))
        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()
        customer_address = self.textEdit_2.toPlainText()
        total = self.lineEdit_17.text()
        igst = self.lineEdit_14.text()
        bill_number = self.Bill_Number
        self.invoice_list = self.l
        self.docGSTInvoice.render({
            "bill_no": bill_number,
            "date": current_date,
            "name": customer_Name, 
            "email": customer_Email,
            "contact": contact_number,
            "address": customer_address,
            "total": total,
            "igst" : igst,
            "item_list": self.invoice_list
            })
        self.docGSTInvoice.save("Billing_Saved_Data/"+"invoice-"+str(self.Bill_Number)+"("+str(self.current_date1)+").docx")
   
    def invoice(self):
        current_date = str("%s:%s:%s" % (self.dt.day, self.dt.month, self.dt.year))
        customer_Name = self.lineEdit_6.text()
        customer_Email = self.lineEdit_8.text()
        contact_number = self.lineEdit_12.text()
        customer_address = self.textEdit_2.toPlainText()
        
        p = float(self.x1.text())*float(self.y1.text())
        q = float(self.x2.text())*float(self.y2.text())
        r = float(self.x3.text())*float(self.y3.text())
        s = float(self.x4.text())*float(self.y4.text())
        t = float(self.x5.text())*float(self.y5.text())
        u = float(self.x6.text())*float(self.y6.text())
        
        total = (p+q+r+s+t+u)
        bill_number = self.Bill_Number
        self.invoice_list = self.l
        self.docInvoice.render({
            "bill_no": bill_number,
            "date": current_date,
            "name": customer_Name, 
            "email": customer_Email,
            "contact": contact_number,
            "address": customer_address,
            "total": total,
            "item_list": self.invoice_list
            })
        self.docInvoice.save("Billing_Saved_Data/"+"invoice-"+str(self.Bill_Number)+"("+str(self.current_date1)+").docx")
        
        
        
        
    def add_customer_purchase(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        customer_name = self.lineEdit_6.text()
        customer_email = self.lineEdit_8.text()
        customer_contact = self.lineEdit_12.text()
        customer_address = self.textEdit_2.toPlainText()
        total_purchase = self.lineEdit_17.text()
        purchase_bill_no = self.Bill_Number
        purchase_date = self.current_date2
        
        try:
            data = (customer_name,customer_email,customer_contact,customer_address,total_purchase,purchase_bill_no,purchase_date)
            sql = ''' INSERT INTO customer_purchase VALUES (?,?,?,?,?,?,?) '''
            self.cur.execute(sql,data)
            self.db.commit()
            self.db.close()
        except Exception as e:
            buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}")
        
        
        pass