from time import time
from turtle import update
import requests
import pandas as pd
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import * 

class Access_API: # Class to do RESTful operations
    def __init__(self):
        api_url = "https://api.spacexdata.com/v3/launches" 
        response = requests.get(api_url)
        self.result = response.json()

class Data_SRC: #Use like Data Access Object
    def __init__(self):
        access_api = Access_API()
        dateframe = pd.json_normalize(access_api.result) #This is a Nested JSON
        dateframe.columns = dateframe.columns.map(lambda x: x.split(".")[-1])
        self.result = dateframe

    def frequentlyYear(self): #Years that most appear
        year_most_frequently = self.result['launch_year'].value_counts().idxmax()
        return(year_most_frequently)

    def launcSite(self): #Launch site with most launchs
        launch_site =  self.result['site_name_long'].value_counts().idxmax()
        return str(launch_site)
    
    def totalLaunch(self): #Total of Launchs between 19-21
        total_launch =  self.result.loc[( self.result['launch_year'] > '2018') & ( self.result['launch_year'] < '2022' )].count()
        return(total_launch['flight_number'])

class Create_XLSX: #Create an Excel file
    def __init__(self,directory, filename):
        select_data = Data_SRC()
        
        data_file = {
             'Ano com mais lancamentos': [select_data.frequentlyYear()] , 
             'Local com mais lancamentos': [str(select_data.launcSite())] ,
             'Total de Lancamentos entre 2019 e 2021' : [select_data.totalLaunch()]
            }
        fullname = directory + r"/" + filename + '.xlsx'
        df = pd.DataFrame.from_dict(data_file)
        df.to_excel(fullname ,index = False)


class Front_End: #Create a FrontEnd View
    def __init__(self):
        app = QApplication(sys.argv)
        widget = QWidget()
        self.app = QApplication(sys.argv)
        self.widget = QWidget()
        ui = Ui_Dialog()
        ui.setupUi(self.widget)
        self.widget.show()
        sys.exit(app.exec_())

class Ui_Dialog(object): # Generate FronEnd View
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(476, 252)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setGeometry(QtCore.QRect(110, 160, 337, 31))
        self.textEdit.setObjectName("textEdit")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(160, 210, 211, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.generateFile) #Generate File
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(40, 160, 61, 31))
        self.label.setObjectName("label")
        self.graphicsView = QtWidgets.QGraphicsView(Dialog)
        self.graphicsView.setGeometry(QtCore.QRect(-48, -50, 529, 311))
        self.graphicsView.setStyleSheet("image: url(:/images/xplayout.jpg);")
        self.graphicsView.setObjectName("graphicsView")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 61, 31))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(112, 10, 97, 101))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setText("")
        self.label_3.setTextFormat(QtCore.Qt.PlainText)
        self.label_3.setPixmap(QtGui.QPixmap("icon.png"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(368, 120, 81, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.browserPath) #Search by Directory 
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(224, 20, 129, 81))
        self.label_4.setText("")
        self.label_4.setTextFormat(QtCore.Qt.PlainText)
        self.label_4.setPixmap(QtGui.QPixmap("space-X.png"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(112, 120, 241, 31))
        self.textEdit_2.setObjectName("textEdit_2")
        self.progressBar = QtWidgets.QProgressBar(Dialog)
        self.progressBar.setGeometry(QtCore.QRect(16, 220, 97, 20))
        self.progressBar.setObjectName("progressBar")
        self.graphicsView.raise_()
        self.pushButton.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.textEdit.raise_()
        self.pushButton_2.raise_()
        self.label_4.raise_()
        self.textEdit_2.raise_()
        self.msg = QMessageBox()
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def browserPath(self,folderpath): #Get the folder directory
        folderpath = str(QtWidgets.QFileDialog.getExistingDirectory(None,"Choose Directory"))
        self.textEdit_2.setText(folderpath)

    def generateFile(self):#Gererate the file using the name and directory
        directory = self.textEdit_2.toPlainText()
        filename = self.textEdit.toPlainText()
        if directory == "" or filename == "":
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("Please, fill Directory and Filename")
            self.msg.setWindowTitle("Information")
            self.msg.exec_()
        else:
            self.textEdit.hide()
            self.pushButton.hide()
            self.label_2.hide()
            self.pushButton_2.hide()
            self.textEdit_2.hide()

            self.label.setGeometry(QtCore.QRect(190, 100, 150, 100))
            self.label.setText("Loading...")

            self.label.setFont(QtGui.QFont('Arial', 20))

            QApplication.processEvents()

            Create_XLSX(directory ,filename).__init__
            self.msg.setIcon(QMessageBox.Information)
            self.msg.setText("File created sucessfully")
            self.msg.setWindowTitle("Information")
            self.msg.exec_()

            self.label.setGeometry(QtCore.QRect(40, 160, 61, 31))
            self.label.setText("File Name")
            self.label.setFont(QtGui.QFont())

            self.textEdit.show()
            self.pushButton.show()
            self.label_2.show()
            self.pushButton_2.show()
            self.textEdit_2.show()
            QApplication.processEvents()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Launch Application"))
        self.pushButton.setText(_translate("Dialog", "Generate File"))
        self.label.setText(_translate("Dialog", "File Name"))
        self.label_2.setText(_translate("Dialog", "Directory"))
        self.pushButton_2.setText(_translate("Dialog", "Browser..."))

generate_app = Front_End()