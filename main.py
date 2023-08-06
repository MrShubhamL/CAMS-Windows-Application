from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sqlite3
from tkinter import *
from PyQt5 import QtGui,QtCore,QtWidgets
from PyQt5.uic import loadUiType
import sys
import Flash_window
import urllib.request
import pyotp
import qrcode

zi,_ = loadUiType('Login_gui.ui')
class Login(QWidget,zi):                # Login Code....
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.login_button.clicked.connect(self.Handel_Login)
        self.close_button.clicked.connect(self.Exit)
        self.pushButton_5.clicked.connect(self.sign_up)
        self.pushButton_4.clicked.connect(self.forgot_pass)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background-image : url(assets/login_img.png);")

        
    def Handel_Login(self):
        self.flash = Flash_window.Screen()
        self.flash.show()
        self.close()
    
    def sign_up(self):
        self.signup = SignUp()
        self.signup.show()
        self.close()
    
    def forgot_pass(self):
        try:
            urllib.request.urlopen("http://google.com") 
            self.forgot = ForgotPassOTP()
            self.forgot.show()
            self.close()#Python 3.x
        except:
            buttonReply = QMessageBox.information(self, "No Internet","Please connect with Internet")
    

    
    
    def Exit(self):
        sys.exit(Login)


    
    
ci,_ = loadUiType('SignUp.ui')
class SignUp(QWidget,ci):                # Login Code....
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background-image : url(assets/login_img.png);")
        self.handelButton()
        
    def handelButton(self):
        self.pushButton_5.clicked.connect(self.login_window)
        self.signup_button.clicked.connect(self.create_new_user)
        self.close_button.clicked.connect(self.Exit)
        pass
    
    def login_window(self):
        self.login = Login()
        self.login.show()
        self.close()
        pass
    
    def create_new_user(self):
        Username = self.username_input.text()
        Password = self.password_input.text()
        Password_2 = self.password_input_2.text()
        
        if Username == "" and Password == "" and Password_2 =="":  
            buttonReply = QMessageBox.information(self, "Invalid!","All fields are required!")
        elif Password != Password_2:
            buttonReply = QMessageBox.information(self, "Invalid!","Password is not matched!")
        else:
            self.db = sqlite3.connect('DB\db.db')
            self.cur = self.db.cursor()
            try:
                data = (Username,Password)
                sql = ''' INSERT INTO user VALUES (?,?) '''
                self.cur.execute(sql,data)
                self.db.commit()
                self.db.close()
                warning = QMessageBox.warning(self , 'Account Created!' , "Account created successfully." , QMessageBox.Yes | QMessageBox.No)
                if warning == QMessageBox.Yes :
                    self.login_window()
                else:
                    self.login_window()
            except Exception as e:
                buttonreplay = QMessageBox.information(self,"Sorry!",f"Application Error Occured - {e}")

    def Exit(self):
        sys.exit(Login)
    
fi,_ = loadUiType('forgot_pass_auth.ui')
class ForgotPassOTP(QWidget,fi):                # Login Code....
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background-image : url(assets/login_img.png);")
        self.qr_code_frame.setStyleSheet("""
                                         background-image : url(AuthQR/fpac.png);
                                         background-position: center;
                                         """)
        self.buttonHandel()
       
    def buttonHandel(self):
        self.submit_button.clicked.connect(self.check_otp)
        self.pushButton_5.clicked.connect(self.loginWindow)
        self.close_button.clicked.connect(self.Exit)
    
    def loginWindow(self):
        self.login = Login()
        self.login.show()
        self.close()
        
    def check_otp(self):
        key = "NeuralNineMySuperSecretKey"
        totp = pyotp.TOTP(key)

        pyotp.totp.TOTP(key).provisioning_uri(name = "HariomEnterprises877",
                                                    issuer_name="Computer Management App")
        # qrcode.make(uri).save("AUthQR/totp.png")
        _otp = self.otp_input.text()
        if totp.verify(_otp):
            self.forgot_window = ForgotPassWindow()
            self.forgot_window.show()
            self.close()
        else:
            buttonReply = QMessageBox.information(self, "Invalid!","OTP is not correct!")
            
    def Exit(self):
        sys.exit(Login)          
            
ki,_ = loadUiType('forgot_pass_window.ui')
class ForgotPassWindow(QWidget,ki):                # Login Code....
    def __init__(self):
        QWidget.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.ico'))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background-image : url(assets/login_img.png);")
        self.ButtonHandel()
        
        
    def ButtonHandel(self):
        self.reset_button.clicked.connect(self.reset_password)
        self.close_button.clicked.connect(self.Exit)
            
    
    def reset_password(self):
        self.db = sqlite3.connect('DB\db.db')
        self.cur = self.db.cursor()
        
        self.username = self.username.text()
        self.password  = self.password.text()
        self.confirm_password = self.confirm_password.text()
        
        if self.username == "":
            d = QMessageBox.information(self,"Alert!","Please enter registred username!")
        elif self.password != self.confirm_password:
            d = QMessageBox.information(self,"Information!","Password not matched!")
        else:
            try:
                self.cur.execute(f""" UPDATE user SET Password = '{self.confirm_password}' WHERE Username = '{self.username}' """)
                self.db.commit()
                self.db.close()
                dd = QMessageBox.information(self,"Updated","Password Successfully Reset.",  QMessageBox.Yes | QMessageBox.No)
                if dd == QMessageBox.Yes:
                    self.login = Login()
                    self.login.show()
                    self.close()
                else:
                   self.login = Login()
                   self.login.show()
                   self.close() 
            except Exception as e:
                dfdsfsd = QMessageBox.information(self,"Failed!",f"{e}")
                
    def Exit(self):
        sys.exit(Login)   
        
    
def main():
    app = QtWidgets.QApplication(sys.argv)
    window = Login()
    window.show()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()
   