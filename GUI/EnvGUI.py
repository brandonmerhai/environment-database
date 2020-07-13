# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI3052.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import re
import mysql.connector
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtSql import *
import time
from pandas import *

usr = ""
pwd = ""
sourceFrom = ""
attributeList = ""
stateAttribute = ""
phenomenaAttribute = ""
renewableAttribute = ""
yearlyWeatherAttribute = ""
greenHouseAttribute = ""
airQualityAttribute = ""
waterQualityAttribute = ""
blizzardAttribute = ""
hurricaneAttribute = ""
droughtAttribute = ""

operatorList = ""
stateOperator = ""
phenomenaOperator = ""
renewableOperator = ""
yearlyWeatherOperator = ""
greenHouseOperator = ""
airQualityOperator = ""
waterQualityOperator = ""
blizzardOperator = ""
hurricaneOperator = ""
droughtOperator = ""

stateResult = ""
phenomenaResult = ""
renewableEnergy = ""
yearlyWeatherResult = ""
greenHouseResult = ""
airQualityResult = ""
waterQualityResult = ""
blizzardResult = ""
hurricaneResult = ""
droughtResult = ""

looper = 0



class FormViewWindow(QtWidgets.QMainWindow):
    def _init_(self, parent=None):
        super(FormViewWindow, self)._init_(parent)

    def initWindow(self):
        self.setGeometry(200,200,200,200)
        self.show()

class UpdateDatabase(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(UpdateDatabase, self).__init__(parent)
        self.setWindowTitle("Insert into Database")

        self.leftpane = QtWidgets.QListWidget()
        self.leftpane.insertItem(0, 'State')
        self.leftpane.insertItem(1, 'Hurricane')

        self.p1 = QtWidgets.QWidget()
        self.p2 = QtWidgets.QWidget()

        self.p1UI()
        self.p2UI()

        self.Stack = QtWidgets.QStackedWidget(self)
        self.Stack.addWidget(self.p1)
        self.Stack.addWidget(self.p2)

        hbox = QtWidgets.QHBoxLayout(self)
        hbox.addWidget(self.leftpane)
        hbox.addWidget(self.Stack)

        self.setLayout(hbox)
        self.leftpane.currentRowChanged.connect(self.display)
        self.setGeometry(300, 50, 10, 10)
        self.show()

    def p1UI(self):
        layout = QtWidgets.QFormLayout()
        self.nameUpdate = QtWidgets.QLineEdit()
        self.regionUpdate = QtWidgets.QLineEdit()
        self.populationUpdate = QtWidgets.QLineEdit()
        self.gdpUpdate = QtWidgets.QLineEdit()
        self.updateButton = QtWidgets.QPushButton("Insert")
        self.updateButton.clicked.connect(self.updateState)
        self.cancelButton = QtWidgets.QPushButton("Cancel")
        layout.addRow("Name:", self.nameUpdate)
        layout.addRow("Region:", self.regionUpdate)
        layout.addRow("Population:", self.populationUpdate)
        layout.addRow("GDP:", self.gdpUpdate)
        layout.addRow(self.updateButton, self.cancelButton)
        self.p1.setLayout(layout)

    def p2UI(self):
        layout = QtWidgets.QFormLayout()
        layout.addRow("ID:", QtWidgets.QLineEdit())
        layout.addRow("Hurricane Name:", QtWidgets.QLineEdit())
        self.p2.setLayout(layout)

    def display(self, i):
        self.Stack.setCurrentIndex(i)

    def updateState(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            sqlUpdate = "INSERT INTO State (Name, Region, Population, GDP) VALUES (%s, %s, %s, %s)"
            val = (self.nameUpdate.text(), self.regionUpdate.text(), self.populationUpdate, self.gdpUpdate.text())
            print(val)
            cursor = cnx.cursor()
            cursor.execute(sqlUpdate, val)
            cnx.commit()
            print("Successfully inserted items")
        except Exception as e:
            print("State Table Update Failure")
            print(e)

class StateReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(StateReport, self).__init__(parent)
        self.setWindowTitle("State")
        self.data = ()
        self.maxSize = 2

        global usr
        global pwd

        self.IDLabel = QtWidgets.QLabel("ID:")
        self.IDField = QtWidgets.QLineEdit("")
        self.NameLabel = QtWidgets.QLabel("Name:")
        self.NameField = QtWidgets.QLineEdit("")
        self.RegionLabel = QtWidgets.QLabel("Region:")
        self.RegionField = QtWidgets.QLineEdit("")
        self.GDPLabel = QtWidgets.QLabel("GDP:")
        self.GDPField = QtWidgets.QLineEdit("")

        self.fButton = QtWidgets.QPushButton("Next")
        self.bButton = QtWidgets.QPushButton("Back")
        self.qButton = QtWidgets.QPushButton("Quit")
        self.lButton = QtWidgets.QPushButton("Load")

        self.lButton.clicked.connect(self.loadData)
        self.fButton.clicked.connect(self.nextResult)
        self.bButton.clicked.connect(self.prevResult)
        self.qButton.clicked.connect(self.closeForm)

        layout = QtWidgets.QFormLayout()
        layout.addRow(self.IDLabel, self.IDField)
        layout.addRow(self.NameLabel, self.NameField)
        layout.addRow(self.RegionLabel, self.RegionField)
        layout.addRow(self.GDPLabel, self.GDPField)
        layout.addRow(self.bButton, self.fButton)
        layout.addRow(self.lButton, self.qButton)
        self.setLayout(layout)

    def loadData(self):
        global usr
        global pwd
        global looper

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sqlQuery = "SELECT * FROM State"
            cursor = cnx.cursor(buffered=True)
            cursor.execute(sqlQuery)
            self.data = cursor.fetchall()
            self.maxSize = len(self.data)

            self.IDField.setText(str(self.data[looper][0]))
            self.NameField.setText(str(self.data[looper][1]))
            self.RegionField.setText(str(self.data[looper][2]))
            self.GDPField.setText(str(self.data[looper][3]))

        except:
            print("Failed to connect [stateFormDisplay]")


    def nextResult(self):
        global looper

        looper = looper + 1
        if looper > self.maxSize-1:
            looper = self.maxSize-1

        self.IDField.setText(str(self.data[looper][0]))
        self.NameField.setText(str(self.data[looper][1]))
        self.RegionField.setText(str(self.data[looper][2]))
        self.GDPField.setText(str(self.data[looper][3]))

    def prevResult(self):
        global looper

        looper = looper - 1
        if looper < 0:
            looper = 0

        self.IDField.setText(str(self.data[looper][0]))
        self.NameField.setText(str(self.data[looper][1]))
        self.RegionField.setText(str(self.data[looper][2]))
        self.GDPField.setText(str(self.data[looper][3]))

    def closeForm(self):
        self.close()

class PhenomenaReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(PhenomenaReport, self).__init__(parent)
        self.setWindowTitle("Major Phenomena")

class RenewableReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(RenewableReport, self).__init__(parent)
        self.setWindowTitle("Renewable Energy")

class WeatherReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WeatherReport, self).__init__(parent)
        self.setWindowTitle("Weather")

class GreenHouseReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(GreenHouseReport, self).__init__(parent)
        self.setWindowTitle("Greenhouse Gases")

class AirQualityReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AirQualityReport, self).__init__(parent)
        self.setWindowTitle("Air Quality")

class WaterReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(WaterReport, self).__init__(parent)
        self.setWindowTitle("Water Quality")

class BlizzardReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(BlizzardReport, self).__init__(parent)
        self.setWindowTitle("Blizzard")

class HurricaneReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(HurricaneReport, self).__init__(parent)
        self.setWindowTitle("Hurricane")

class DroughtReport(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(DroughtReport, self).__init__(parent)
        self.setWindowTitle("Drought")

class AboutInfo(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(AboutInfo, self).__init__(parent)
        self.setWindowTitle("About Info")

        self.QAuthorLabel = QtWidgets.QLabel("Created by Brandon Merhai and Jihae Kim")
        self.QYearLabel = QtWidgets.QLabel('                    ISE 305, Fall 2019')
        self.QDisclaimer = QtWidgets.QLabel("Alpha code, no guarantee of functionality.")
        layout = QtWidgets.QFormLayout()
        layout.addRow(self.QAuthorLabel)
        layout.addRow(self.QYearLabel)
        layout.addRow(self.QDisclaimer)

        self.setLayout(layout)

class Form(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Form,self).__init__(parent)

        global usr
        global pwd

        self.username = QtWidgets.QLineEdit(self)
        self.QUserLabel = QtWidgets.QLabel("Username:")
        self.QLabel = QtWidgets.QLabel("Status:")
        self.statusDisplay = QtWidgets.QLabel("Not connected...")

        self.password = QtWidgets.QLineEdit(self)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.QPasswordLabel = QtWidgets.QLabel("Password:")

        self.btn_Submit = QtWidgets.QPushButton("Login")
        self.btn_Disconnect = QtWidgets.QPushButton("Log Out")

        layout = QtWidgets.QFormLayout()
        layout.addRow(self.QUserLabel,self.username)
        layout.addRow(self.QPasswordLabel,self.password)
        layout.addRow(self.btn_Submit, self.btn_Disconnect)
        layout.addRow(self.QLabel, self.statusDisplay)


        self.btn_Submit.clicked.connect(self.login)
        self.btn_Disconnect.clicked.connect(self.logout)

        self.setLayout(layout)

    def login(self):
        global usr
        global pwd
        is_logged_in = False

        try:
            cnx = mysql.connector.connect(user=self.username.text(), password=self.password.text(), host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Database successfully!")
            self.statusDisplay.setText("Logged in successfully!")
            is_logged_in = True
        except:
            print("Could not connect to DB")
            self.statusDisplay.setText("Incorrect credentials...")

        if is_logged_in:
            time.sleep(1)
            usr = self.username.text()
            pwd = self.password.text()
            self.close()

    def logout(self):
        global usr
        global pwd
        is_logged_in = False

        try:
            cnx = mysql.connector.connect(user=self.username.text(), password=self.password.text(), host='127.0.0.1', database='ISE 305 Environment Database')
            cnx.close()
            self.statusDisplay.setText("Disconnected.")
            self.password.setText("")
            self.username.setText("")
            usr = self.username.setText()
            pwd = self.password.sextText()

            time.sleep(1)
            self.close()
        except:
            self.statusDisplay.setText("Not signed in.")
            usr = self.username.setText("")
            pwd = self.password.setText("")

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 1000)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setBaseSize(QtCore.QSize(1280, 1000))
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("#MainWindow{background-image: url(:/background/christian-holzinger-CUY_YHhCFl4-unsplash.jpg);}")
        MainWindow.setDocumentMode(False)
        MainWindow.setDockNestingEnabled(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_3.addWidget(self.pushButton_4)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.gridLayout.addLayout(self.horizontalLayout_3, 7, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_2.addWidget(self.progressBar)
        self.gridLayout.addLayout(self.horizontalLayout_2, 5, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(16)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.checkBox_10 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_10.setObjectName("checkBox_10")
        self.verticalLayout_2.addWidget(self.checkBox_10)
        self.checkBox_2 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_2.setObjectName("checkBox_2")
        self.verticalLayout_2.addWidget(self.checkBox_2)
        """self.checkBox_3 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.verticalLayout_2.addWidget(self.checkBox_3)"""
        self.checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName("checkBox")
        self.verticalLayout_2.addWidget(self.checkBox)
        self.checkBox_4 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.verticalLayout_2.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.verticalLayout_2.addWidget(self.checkBox_5)
        """self.checkBox_6 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.verticalLayout_2.addWidget(self.checkBox_6)"""
        """self.checkBox_7 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_7.setObjectName("checkBox_7")
        self.verticalLayout_2.addWidget(self.checkBox_7)"""
        self.checkBox_8 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_8.setObjectName("checkBox_8")
        self.verticalLayout_2.addWidget(self.checkBox_8)
        self.checkBox_9 = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBox_9.setObjectName("checkBox_9")
        self.verticalLayout_2.addWidget(self.checkBox_9)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_4, 9, 0, 1, 1)
        self.comboBox_7 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_7, 3, 0, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_8, 4, 0, 1, 1)
        """self.comboBox_6 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_6, 2, 0, 1, 1)"""
        self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_5, 1, 0, 1, 1)
        self.comboBox_12 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_12, 8, 0, 1, 1)
        """self.comboBox_10 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_10, 6, 0, 1, 1)"""
        """self.comboBox_11 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_11, 7, 0, 1, 1)"""
        self.comboBox_9 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_9, 5, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setFrame(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 0, 1, 1)
        self.horizontalLayout_5.addLayout(self.gridLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, 0, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_6.setContentsMargins(0, -1, 80, -1)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_2)
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_3)
        """self.comboBox_15 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_15.setObjectName("comboBox_15")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.comboBox_15.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_15)"""
        self.comboBox_17 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_17.setObjectName("comboBox_17")
        self.comboBox_17.addItem("")
        self.comboBox_17.addItem("")
        self.comboBox_17.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_17)
        self.comboBox_18 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_18)
        self.comboBox_19 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_19)
        """self.comboBox_16 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_16.setObjectName("comboBox_16")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.comboBox_16.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_16)"""
        """self.comboBox_14 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_14.setObjectName("comboBox_14")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.comboBox_14.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_14)"""
        self.comboBox_30 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_30.setObjectName("comboBox_30")
        self.comboBox_30.addItem("")
        self.comboBox_30.addItem("")
        self.comboBox_30.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_30)
        self.comboBox_13 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.verticalLayout_6.addWidget(self.comboBox_13)
        self.horizontalLayout.addLayout(self.verticalLayout_6)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_4.setContentsMargins(-1, -1, 0, -1)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.horizontalLayout_6.addWidget(self.lineEdit_2)
        self.comboBox_20 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_20.setObjectName("comboBox_20")
        self.comboBox_20.addItem("")
        self.comboBox_20.addItem("")
        self.horizontalLayout_6.addWidget(self.comboBox_20)
        self.verticalLayout_4.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_7.addWidget(self.lineEdit_4)
        self.comboBox_24 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_24.setObjectName("comboBox_24")
        self.comboBox_24.addItem("")
        self.comboBox_24.addItem("")
        self.horizontalLayout_7.addWidget(self.comboBox_24)
        self.verticalLayout_4.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        """self.lineEdit_6 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.horizontalLayout_8.addWidget(self.lineEdit_6)"""
        """self.comboBox_28 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_28.setObjectName("comboBox_28")
        self.comboBox_28.addItem("")
        self.comboBox_28.addItem("")
        self.horizontalLayout_8.addWidget(self.comboBox_28)"""
        self.verticalLayout_4.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_9.addWidget(self.lineEdit_7)
        self.comboBox_27 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_27.setObjectName("comboBox_27")
        self.comboBox_27.addItem("")
        self.comboBox_27.addItem("")
        self.horizontalLayout_9.addWidget(self.comboBox_27)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.horizontalLayout_10.addWidget(self.lineEdit_9)
        self.comboBox_26 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_26.setObjectName("comboBox_26")
        self.comboBox_26.addItem("")
        self.comboBox_26.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox_26)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.horizontalLayout_11.addWidget(self.lineEdit_8)
        self.comboBox_25 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_25.setObjectName("comboBox_25")
        self.comboBox_25.addItem("")
        self.comboBox_25.addItem("")
        self.horizontalLayout_11.addWidget(self.comboBox_25)
        self.verticalLayout_4.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        """self.lineEdit_5 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_12.addWidget(self.lineEdit_5)"""
        """self.comboBox_23 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_23.setObjectName("comboBox_23")
        self.comboBox_23.addItem("")
        self.comboBox_23.addItem("")
        self.horizontalLayout_12.addWidget(self.comboBox_23)"""
        self.verticalLayout_4.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        """self.lineEdit_3 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.horizontalLayout_13.addWidget(self.lineEdit_3)
        self.comboBox_22 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_22.setObjectName("comboBox_22")
        self.comboBox_22.addItem("")
        self.comboBox_22.addItem("")
        self.horizontalLayout_13.addWidget(self.comboBox_22)"""
        self.verticalLayout_4.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setContentsMargins(0, 10, -1, -1)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.horizontalLayout_15.addWidget(self.lineEdit_10)
        self.comboBox_21 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_21.setObjectName("comboBox_21")
        self.comboBox_21.addItem("")
        self.comboBox_21.addItem("")
        self.horizontalLayout_15.addWidget(self.comboBox_21)
        self.verticalLayout_4.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_14.addWidget(self.lineEdit)
        self.comboBox_29 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_29.setObjectName("comboBox_29")
        self.comboBox_29.addItem("")
        self.comboBox_29.addItem("")
        self.horizontalLayout_14.addWidget(self.comboBox_29)
        self.verticalLayout_4.addLayout(self.horizontalLayout_14)
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.horizontalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_16.setContentsMargins(-1, 10, -1, -1)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        self.pushButton.setBaseSize(QtCore.QSize(0, 0))
        self.pushButton.setObjectName("pushButton")
        self.query1 = QtWidgets.QPushButton("Query 1")
        self.query2 = QtWidgets.QPushButton("Query 2")
        self.query3 = QtWidgets.QPushButton("Query 3")
        self.query4 = QtWidgets.QPushButton("Query 4")
        self.query5 = QtWidgets.QPushButton("Query 5")

        self.horizontalLayout_16.addWidget(self.pushButton)
        self.horizontalLayout_16.addWidget(self.query1)
        self.horizontalLayout_16.addWidget(self.query2)
        self.horizontalLayout_16.addWidget(self.query3)
        self.horizontalLayout_16.addWidget(self.query4)
        self.horizontalLayout_16.addWidget(self.query5)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setContentsMargins(0, -1, 400, -1)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.horizontalLayout_16.addLayout(self.horizontalLayout_17)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout_16.addWidget(self.label)
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralwidget)
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.Box)
        self.lcdNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber.setLineWidth(1)
        ##self.lcdNumber.setStyleSheet("background-color: white; color: black;")
        self.lcdNumber.setMidLineWidth(1)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(10)
        self.lcdNumber.setObjectName("lcdNumber")
        self.horizontalLayout_16.addWidget(self.lcdNumber)
        self.verticalLayout.addLayout(self.horizontalLayout_16)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)

        self.horizontalLayout_4.addWidget(self.tableView)
        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 825, 22))
        self.menubar.setMinimumSize(QtCore.QSize(0, 0))
        self.menubar.setBaseSize(QtCore.QSize(825, 20))
        self.menubar.setObjectName("menubar")
        self.menuHome = QtWidgets.QMenu(self.menubar)
        self.menuHome.setSeparatorsCollapsible(False)
        self.menuHome.setToolTipsVisible(False)
        self.menuHome.setObjectName("menuHome")
        self.menuResults = QtWidgets.QMenu(self.menubar)
        self.menuResults.setObjectName("menuResults")
        self.menuForms = QtWidgets.QMenu(self.menubar)
        self.menuForms.setObjectName("menuForms")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuHome.menuAction())
        self.menubar.addAction(self.menuResults.menuAction())
        self.menubar.addAction(self.menuForms.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        insertAction = self.menuHome.addAction("Insert")
        insertAction.triggered.connect(self.show_update_window)

        action = self.menuResults.addAction('Login')
        action.triggered.connect(self.new_window_form)

        action2 = self.menuForms.addAction('State')
        action2.triggered.connect(self.show_state_report)

        action3 = self.menuForms.addAction('Major Phenomena')
        action3.triggered.connect(self.show_phenomena_report)

        action4 = self.menuForms.addAction('Renewable Energy')
        action4.triggered.connect(self.show_renewable_report)

        action5 = self.menuForms.addAction('Yearly Weather')
        action5.triggered.connect(self.show_weather_report)

        action6 = self.menuForms.addAction('Greenhouse Gas Sources')
        action6.triggered.connect(self.show_greenhouse_report)

        action7 = self.menuForms.addAction('Air Quality')
        action7.triggered.connect(self.show_air_report)

        action8 = self.menuForms.addAction('Water Quality')
        action8.triggered.connect(self.show_water_report)

        action9 = self.menuForms.addAction('Blizzard')
        action9.triggered.connect(self.show_blizzard_report)

        action10 = self.menuForms.addAction('Hurricane')
        action10.triggered.connect(self.show_hurricane_report)

        action11 = self.menuForms.addAction('Drought')
        action11.triggered.connect(self.show_drought_report)

        helpAction = self.menuHelp.addAction('About')
        helpAction.triggered.connect(self.show_about_info)

        self.menubar.setNativeMenuBar(False)
        self.dialog = QtWidgets.QDialog(self.centralwidget)
        self.form = Form()
        self.stateReport = StateReport()
        self.phenomenaReport = PhenomenaReport()
        self.renewableReport = RenewableReport()
        self.weatherReport = WeatherReport()
        self.greenHouseReport = GreenHouseReport()
        self.airReport = AirQualityReport()
        self.waterReport = WaterReport()
        self.blizzardReport = BlizzardReport()
        self.hurricaneReport = HurricaneReport()
        self.droughtReport = DroughtReport()
        self.aboutInfo = AboutInfo()
        self.updateWindow = UpdateDatabase()

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ISE305 Environmental Database: Brandon Merhai, Jihae Kim"))
        self.pushButton_3.setText(_translate("MainWindow", "Run Query"))
        self.pushButton_4.setText(_translate("MainWindow", "Reset"))
        self.pushButton_2.setText(_translate("MainWindow", "Quit"))
        self.label_5.setText(_translate("MainWindow", "Progress:"))
        self.tableView.setSortingEnabled(True)
        self.label_2.setText(_translate("MainWindow", "Choose at least one of the following to add to your query:"))
        self.label_2.setFrameShape(QtWidgets.QFrame.Panel)
        #self.label_2.setStyleSheet("background-color: white;")
        self.checkBox_10.setText(_translate("MainWindow", "State"))
        self.checkBox_2.setText(_translate("MainWindow", "CBSA"))
        """self.checkBox_3.setText(_translate("MainWindow", "RenewableEnergyUsage"))"""
        self.checkBox.setText(_translate("MainWindow", "Yearly Weather"))
        self.checkBox_4.setText(_translate("MainWindow", "Energy"))
        self.checkBox_5.setText(_translate("MainWindow", "AQI"))
        """self.checkBox_6.setText(_translate("MainWindow", "Water Quality"))"""
        """self.checkBox_7.setText(_translate("MainWindow", "Blizzard"))"""
        self.checkBox_8.setText(_translate("MainWindow", "Hurricane"))
        self.checkBox_9.setText(_translate("MainWindow", "Drought"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "droughtID"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "none"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "state"))
        self.comboBox_4.setItemText(3, _translate("MainWindow", "dry"))
        self.comboBox_4.setItemText(4, _translate("MainWindow", "moderate"))
        self.comboBox_4.setItemText(5, _translate("MainWindow", "severe"))
        self.comboBox_4.setItemText(6, _translate("MainWindow", "extreme"))
        self.comboBox_4.setItemText(7, _translate("MainWindow", "worst"))
        self.comboBox_4.setItemText(8, _translate("MainWindow", "startDate"))
        self.comboBox_4.setItemText(9, _translate("MainWindow", "endDate"))
        self.comboBox_7.setItemText(0, _translate("MainWindow", "State"))
        self.comboBox_7.setItemText(1, _translate("MainWindow", "Avg F"))
        self.comboBox_7.setItemText(2, _translate("MainWindow", "Avg C"))
        self.comboBox_7.setItemText(3, _translate("MainWindow", "Rain IN"))
        self.comboBox_7.setItemText(4, _translate("MainWindow", "Rain MM"))
        self.comboBox_7.setItemText(5, _translate("MainWindow", "Days of Snow"))
        self.comboBox_7.setItemText(6, _translate("MainWindow", "Snow IN"))
        self.comboBox_7.setItemText(7, _translate("MainWindow", "Snow CM"))
        self.comboBox_7.setItemText(8, _translate("MainWindow", "Humidity AM"))
        self.comboBox_7.setItemText(9, _translate("MainWindow", "Humidity PM"))
        self.comboBox_7.setItemText(10, _translate("MainWindow", "% Sun"))
        self.comboBox_7.setItemText(11, _translate("MainWindow", "Total Hours Sunlight"))
        self.comboBox_7.setItemText(12, _translate("MainWindow", "Clear Days"))
        self.comboBox_7.setItemText(13, _translate("MainWindow", "stateAB"))
        self.comboBox_8.setItemText(0, _translate("MainWindow", "ID"))
        self.comboBox_8.setItemText(1, _translate("MainWindow", "State"))
        self.comboBox_8.setItemText(2, _translate("MainWindow", "Year"))
        self.comboBox_8.setItemText(3, _translate("MainWindow", "Type of Producer"))
        self.comboBox_8.setItemText(4, _translate("MainWindow", "Energy Source"))
        self.comboBox_8.setItemText(5, _translate("MainWindow", "Generation"))
        """self.comboBox_6.setItemText(0, _translate("MainWindow", "solar"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "wind"))
        self.comboBox_6.setItemText(2, _translate("MainWindow", "hydroelectric"))
        self.comboBox_6.setItemText(3, _translate("MainWindow", "tidal"))"""
        self.comboBox_5.setItemText(0, _translate("MainWindow", "cbsa_Code"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "cbsa"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "state"))
        self.comboBox_12.setItemText(0, _translate("MainWindow", "Name"))
        self.comboBox_12.setItemText(1, _translate("MainWindow", "Region"))
        self.comboBox_12.setItemText(2, _translate("MainWindow", "Max_Wind_Speed"))
        self.comboBox_12.setItemText(3, _translate("MainWindow", "Min_Pressure"))
        self.comboBox_12.setItemText(4, _translate("MainWindow", "Latitude"))
        self.comboBox_12.setItemText(5, _translate("MainWindow", "Longitude"))
        self.comboBox_9.setItemText(0, _translate("MainWindow", "ID"))
        self.comboBox_9.setItemText(1, _translate("MainWindow", "90th_Percentile_AQI"))
        self.comboBox_9.setItemText(2, _translate("MainWindow", "CBSA"))
        self.comboBox_9.setItemText(3, _translate("MainWindow", "CBSA_Code"))
        self.comboBox_9.setItemText(4, _translate("MainWindow", "Days_CO"))
        self.comboBox_9.setItemText(5, _translate("MainWindow", "Days_NO2"))
        self.comboBox_9.setItemText(6, _translate("MainWindow", "Days_Ozone"))
        self.comboBox_9.setItemText(7, _translate("MainWindow", "Days_PM10"))
        self.comboBox_9.setItemText(8, _translate("MainWindow", "Days_PM2.5"))
        self.comboBox_9.setItemText(9, _translate("MainWindow", "Days_SO2"))
        self.comboBox_9.setItemText(10, _translate("MainWindow", "Days_with_AQI"))
        self.comboBox_9.setItemText(11, _translate("MainWindow", "Good_Days"))
        self.comboBox_9.setItemText(12, _translate("MainWindow", "Hazardous_Days"))
        self.comboBox_9.setItemText(13, _translate("MainWindow", "Max_AQI"))
        self.comboBox_9.setItemText(14, _translate("MainWindow", "Median_AQI"))
        self.comboBox_9.setItemText(15, _translate("MainWindow", "Moderate_Days"))
        self.comboBox_9.setItemText(16, _translate("MainWindow", "Unhealthy_Days"))
        self.comboBox_9.setItemText(17, _translate("MainWindow", "Unhealthy_for_Sensitive_Groups_Days"))
        self.comboBox_9.setItemText(18, _translate("MainWindow", "VeryUnhealthy_Days"))
        self.comboBox_9.setItemText(19, _translate("MainWindow", "Year"))
        self.comboBox.setCurrentText(_translate("MainWindow", "name"))
        self.comboBox.setItemText(0, _translate("MainWindow", "name"))
        self.comboBox.setItemText(1, _translate("MainWindow", "region"))
        self.comboBox.setItemText(2, _translate("MainWindow", "population"))
        self.comboBox.setItemText(3, _translate("MainWindow", "GDP"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_2.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_2.setItemText(2, _translate("MainWindow", "<"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_3.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_3.setItemText(2, _translate("MainWindow", "<"))
        """self.comboBox_15.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_15.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_15.setItemText(2, _translate("MainWindow", "<"))"""
        self.comboBox_17.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_17.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_17.setItemText(2, _translate("MainWindow", "<"))
        self.comboBox_18.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_18.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_18.setItemText(2, _translate("MainWindow", "<"))
        self.comboBox_19.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_19.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_19.setItemText(2, _translate("MainWindow", "<"))
        """self.comboBox_16.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_16.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_16.setItemText(2, _translate("MainWindow", "<"))"""
        """self.comboBox_14.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_14.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_14.setItemText(2, _translate("MainWindow", "<"))"""
        self.comboBox_30.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_30.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_30.setItemText(2, _translate("MainWindow", "<"))
        self.comboBox_13.setItemText(0, _translate("MainWindow", "="))
        self.comboBox_13.setItemText(1, _translate("MainWindow", ">"))
        self.comboBox_13.setItemText(2, _translate("MainWindow", "<"))
        self.comboBox_20.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_20.setItemText(1, _translate("MainWindow", "or"))
        self.comboBox_24.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_24.setItemText(1, _translate("MainWindow", "or"))
        """self.comboBox_28.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_28.setItemText(1, _translate("MainWindow", "or"))"""
        self.comboBox_27.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_27.setItemText(1, _translate("MainWindow", "or"))
        self.comboBox_26.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_26.setItemText(1, _translate("MainWindow", "or"))
        self.comboBox_25.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_25.setItemText(1, _translate("MainWindow", "or"))
        """self.comboBox_23.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_23.setItemText(1, _translate("MainWindow", "or"))"""
        """self.comboBox_22.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_22.setItemText(1, _translate("MainWindow", "or"))"""
        self.comboBox_21.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_21.setItemText(1, _translate("MainWindow", "or"))
        self.comboBox_29.setItemText(0, _translate("MainWindow", "and"))
        self.comboBox_29.setItemText(1, _translate("MainWindow", "or"))
        self.pushButton.setText(_translate("MainWindow", "Add to Query"))
        self.label.setText(_translate("MainWindow", "# of Queries:"))
        self.menuHome.setTitle(_translate("MainWindow", "Home"))
        self.menuResults.setTitle(_translate("MainWindow", "Database"))
        self.menuForms.setTitle(_translate("MainWindow", "Forms"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))


        self.centralwidget.setStyleSheet(
        """
        QComboBox::item{
        height: 12px;
        border: 0px solid #32414B;
        margin-top: 0px;
        margin-bottom: 8px;
        padding: 4px;
        padding-left: 0px;
        }

        """
        )
        self.comboBox_2.setStyleSheet("")
        self.comboBox_3.setStyleSheet("")
        self.comboBox_4.setStyleSheet("")
        self.comboBox_5.setStyleSheet("")
        """self.comboBox_6.setStyleSheet("")"""
        self.comboBox_7.setStyleSheet("")
        self.comboBox_8.setStyleSheet("")
        self.comboBox_9.setStyleSheet("")
        """self.comboBox_10.setStyleSheet("")"""
        """self.comboBox_11.setStyleSheet("")"""
        self.comboBox_12.setStyleSheet("")
        self.comboBox_13.setStyleSheet("")
        """self.comboBox_14.setStyleSheet("")"""
        """self.comboBox_15.setStyleSheet("")"""
        """self.comboBox_16.setStyleSheet("")"""
        self.comboBox_17.setStyleSheet("")
        self.comboBox_18.setStyleSheet("")
        self.comboBox_19.setStyleSheet("")
        self.comboBox_20.setStyleSheet("")
        self.comboBox_21.setStyleSheet("")
        """self.comboBox_22.setStyleSheet("")"""
        """self.comboBox_23.setStyleSheet("")"""
        """self.comboBox_24.setStyleSheet("")"""
        self.comboBox_25.setStyleSheet("")
        self.comboBox_26.setStyleSheet("")
        self.comboBox_27.setStyleSheet("")
        """self.comboBox_28.setStyleSheet("")"""
        self.comboBox_29.setStyleSheet("")
        self.comboBox_30.setStyleSheet("")

        self.pushButton_2.clicked.connect(self.exit_button)
        self.pushButton.clicked.connect(self.add_to_query)
        self.pushButton_3.clicked.connect(self.execute_query)
        self.pushButton_4.clicked.connect(self.reset_query)
        self.query1.clicked.connect(self.query_1_button)
        self.query2.clicked.connect(self.query_2_button)
        self.query3.clicked.connect(self.query_3_button)
        self.query4.clicked.connect(self.query_4_button)
        self.query5.clicked.connect(self.query_5_button)

    def exit_button(self):
        sys.exit()

    def query_1_button(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sql = "SELECT region, SUM(population) AS `Total Population`, COUNT(region) AS `Number of States`, FLOOR(SUM(population)/COUNT(region))  AS `Average Population` FROM State GROUP BY region ORDER BY SUM(population) DESC;"
            df = pandas.read_sql_query(sql, cnx)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
        except Exception as e:
            print(e)

    def query_2_button(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sql = "SELECT `yearly weather`.State, `yearly weather`.`Clear Days`, state.gdp AS `GDP`, `yearly weather`.`humidity AM` AS `Morning Humidity`, `yearly weather`.`Rain IN` AS `Rainfall`, `yearly weather`.`Snow IN` AS `Snowfall`, `yearly weather`.`Total Hours Sunlight`, state.population/state.GDP AS `GDP Per Person`, `yearly weather`.`Avg F` AS `Average Temperature` FROM `yearly weather` INNER JOIN state ON state.stateAB = `yearly weather`.stateAB ORDER BY state.population/state.gdp DESC;"
            df = pandas.read_sql_query(sql, cnx)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
        except Exception as e:
            print(e)

    def query_3_button(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sql = "SELECT State.Name, SUM(generation) AS `Nuclear Generation`, State.GDP, State.GDP/State.Population AS `Per Person` FROM ((State INNER JOIN `Yearly Weather` ON State.stateAB=`Yearly Weather`.stateAB)INNER JOIN Energy ON State.stateAB = Energy.State) WHERE Energy.`Energy Source` = 'Nuclear' GROUP BY State.Name, Energy.`Energy Source`, State.GDP, State.GDP/State.Population ORDER BY State.GDP/State.Population DESC;"
            df = pandas.read_sql_query(sql, cnx)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
        except Exception as e:
            print(e)

    def query_4_button(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sql = "SELECT State.Name, drought.droughtID, drought.worst, drought.startDate, drought.endDate FROM State INNER JOIN drought ON State.stateAB = drought.state WHERE drought.worst > 0 AND Convert(drought.startDate, DATE) >= CONVERT('2018-12-01', DATE) ORDER BY drought.startDate ASC;"
            df = pandas.read_sql_query(sql, cnx)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
        except Exception as e:
            print(e)

    def query_5_button(self):
        global usr
        global pwd

        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            sql = "SELECT newAQI.state, newAQI.avgAQI, `Yearly Weather`.`avg F` FROM (SELECT CBSA.state, ROUND(AVG(AQI.Median_AQI)) AS avgAQI FROM CBSA INNER JOIN AQI ON CBSA.`cbsa Code` = AQI.cbsa_Code GROUP BY CBSA.state) AS newAQI INNER JOIN `Yearly Weather` ON newAQI.state = `Yearly Weather`.state;"
            df = pandas.read_sql_query(sql, cnx)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
        except Exception as e:
            print(e)


    def new_window_form(self):
        self.form.show()

    def show_state_report(self):
        self.stateReport.show()

    def show_phenomena_report(self):
        self.phenomenaReport.show()

    def show_renewable_report(self):
        self.renewableReport.show()

    def show_weather_report(self):
        self.weatherReport.show()

    def show_greenhouse_report(self):
        self.greenHouseReport.show()

    def show_air_report(self):
        self.airReport.show()

    def show_water_report(self):
        self.waterReport.show()

    def show_blizzard_report(self):
        self.blizzardReport.show()

    def show_hurricane_report(self):
        self.hurricaneReport.show()

    def show_drought_report(self):
        self.droughtReport.show()

    def show_about_info(self):
        self.aboutInfo.show()

    def show_update_window(self):
        self.updateWindow.show()

    def add_to_query(self):
        global sourceFrom
        global stateAttribute
        global phenomenaAttribute
        global renewableAttribute
        global yearlyWeatherAttribute
        global greenHouseAttribute
        global airQualityAttribute
        global waterQualityAttribute
        global blizzardAttribute
        global hurricaneAttribute
        global droughtAttribute

        global operatorList
        global stateOperator
        global phenomenaOperator
        global renewableOperator
        global yearlyWeatherOperator
        global greenHouseOperator
        global airQualityOperator
        global waterQualityOperator
        global blizzardOperator
        global hurricaneOperator
        global droughtOperator

        global operatorList
        global stateResult
        global phenomenaResult
        global renewableEnergy
        global yearlyWeatherResult
        global greenHouseResult
        global airQualityResult
        global waterQualityResult
        global blizzardResult
        global hurricaneResult
        global droughtResult



        if self.checkBox_10.isChecked():
            sourceFrom = sourceFrom + ",`State`"
            stateResult = self.lineEdit_2.text()
            stateAttribute = str(self.comboBox.currentText())
            stateOperator = str(self.comboBox_2.currentText())
            stateModifier = str(self.comboBox_24.currentText())

            print(stateResult)
            print(stateAttribute)
            print(stateOperator)
            print(stateModifier)

            #finally


        if self.checkBox_2.isChecked():
            sourceFrom = sourceFrom + ",`CBSA``"
            phenomenaResult = self.lineEdit_4.text()
            phenomenaAttribute = str(self.comboBox_5.currentText())
            phenomenaOperator = str(self.comboBox_3.currentText())
            phenomenaModifier = str(self.comboBox_24.currentText())

            print(phenomenaResult)
            print(phenomenaAttribute)
            print(phenomenaOperator)
            print(phenomenaModifier)

            #finally

        """
        if self.checkBox_3.isChecked():
            sourceFrom = sourceFrom + ",RenewableEnergyUsage"
            renewableEnergy = self.lineEdit_6.text()
            renewableAttribute = str(self.comboBox_6.currentText())
            renewableOperator = str(self.comboBox_15.currentText())
            renewableModifier = str(self.comboBox_28.currentText())
            print(renewableEnergy)
            print(renewableAttribute)
            print(renewableOperator)
            print(renewableModifier)

            #finally
        """

        if self.checkBox.isChecked():
            sourceFrom = sourceFrom + ",`Yearly Weather`"
            yearlyWeatherResult = self.lineEdit_7.text()
            yearlyWeatherAttribute = "`"+str(self.comboBox_7.currentText())+"`"
            yearlyWeatherOperator = str(self.comboBox_17.currentText())
            yearlyWeatherModifier = str(self.comboBox_27.currentText())
            print(yearlyWeatherResult)
            print(yearlyWeatherAttribute)
            print(yearlyWeatherOperator)
            print(yearlyWeatherModifier)

            #finally


        if self.checkBox_4.isChecked():
            sourceFrom = sourceFrom + ",`Energy`"
            greenHouseResult = self.lineEdit_9.text()
            greenHouseAttribute = str(self.comboBox_8.currentText())
            greenHouseOperator = str(self.comboBox_18.currentText())
            greenHouseModifier = str(self.comboBox_26.currentText())
            print(greenHouseResult)
            print(greenHouseAttribute)
            print(greenHouseOperator)
            print(greenHouseModifier)

            #finally


        if self.checkBox_5.isChecked():
            sourceFrom = sourceFrom + ",`AQI`"
            airQualityResult = self.lineEdit_8.text()
            airQualityAttribute = str(self.comboBox_9.currentText())
            airQualityOperator = str(self.comboBox_19.currentText())
            airQualityModifier = str(self.comboBox_25.currentText())
            print(airQualityResult)
            print(airQualityAttribute)
            print(airQualityOperator)
            print(airQualityModifier)

            #finally

        """
        if self.checkBox_6.isChecked():
            sourceFrom = sourceFrom + ",Water Quality"
            waterQualityResult = self.lineEdit_5.text()
            waterQualityAttribute = str(self.comboBox_10.currentText())
            waterQualityOperator = str(self.comboBox_16.currentText())
            waterQualityModifier = str(self.comboBox_23.currentText())
            print(waterQualityResult)
            print(waterQualityAttribute)
            print(waterQualityOperator)
            print(waterQualityModifier)

            #finally
        """

        """if self.checkBox_7.isChecked():
            sourceFrom = sourceFrom + ",Blizzard"
            blizzardResult = self.lineEdit_3.text()
            blizzardAttribute = str(self.comboBox_11.currentText())
            blizzardOperator = str(self.comboBox_14.currentText())
            blizzardModifier = str(self.comboBox_22.currentText())
            print(blizzardResult)
            print(blizzardAttribute)
            print(blizzardOperator)
            print(blizzardModifier)
"""


        if self.checkBox_8.isChecked():
            sourceFrom = sourceFrom + ",`Hurricane`"
            hurricaneResult = self.lineEdit_10.text()
            hurricaneAttribute = str(self.comboBox_12.currentText())
            hurricaneOperator = str(self.comboBox_30.currentText())
            hurricaneModifier = str(self.comboBox_21.currentText())
            print(hurricaneResult)
            print(hurricaneAttribute)
            print(hurricaneOperator)
            print(hurricaneModifier)

            #finally


        if self.checkBox_9.isChecked():
            sourceFrom = sourceFrom + ",`Drought`"
            droughtResult = self.lineEdit.text()
            droughtAttribute = str(self.comboBox_4.currentText())
            droughtOperator = str(self.comboBox_13.currentText())
            droughtModifier = str(self.comboBox_29.currentText())
            print(droughtResult)
            print(droughtAttribute)
            print(droughtOperator)
            print(droughtModifier)

            #finally


        return 0

    def execute_query(self):
        """

        Adds functionality for retrieving modified elements after add_to_query is called and accessing connected MySQL DB to execute.
        Updates and displays the number of queries ran since program start (or reset via clear_queries).

        """
        global countOperations
        global usr
        global pwd
        global sourceFrom
        global attributeList
        global operatorList

        global stateAttribute
        global phenomenaAttribute
        global renewableAttribute
        global yearlyWeatherAttribute
        global greenHouseAttribute
        global airQualityAttribute
        global waterQualityAttribute
        global blizzardAttribute
        global hurricaneAttribute
        global droughtAttribute

        global stateOperator
        global phenomenaOperator
        global renewableOperator
        global yearlyWeatherOperator
        global greenHouseOperator
        global airQualityOperator
        global waterQualityOperator
        global blizzardOperator
        global hurricaneOperator
        global droughtOperator

        global stateResult
        global phenomenaResult
        global renewableEnergy
        global yearlyWeatherResult
        global greenHouseResult
        global airQualityResult
        global waterQualityResult
        global blizzardResult
        global hurricaneResult
        global droughtResult



        try:
            cnx = mysql.connector.connect(user=usr, password=pwd, host='127.0.0.1', database='ISE 305 Environment Database')
            print("Connected to Test Database successfully!")
            self.progressBar.setValue(10)

            cursor = cnx.cursor(buffered=True)
            self.progressBar.setValue(20)

            if self.checkBox_10.isChecked():
                attributeList = attributeList + ","+stateAttribute
                operatorList = " AND "+stateAttribute + stateOperator + stateResult

            if self.checkBox_2.isChecked():
                attributeList = attributeList + ","+phenomenaAttribute
                operatorList = " AND "+phenomenaAttribute + phenomenaOperator + phenomenaResult
            """
            if self.checkBox_3.isChecked():
                attributeList = attributeList + ","+renewableAttribute
                operatorList = " AND "+renewableAttribute + renewableOperator + renewableEnergy
            """
            if self.checkBox.isChecked():
                attributeList = attributeList + ","+yearlyWeatherAttribute
                operatorList = " AND "+yearlyWeatherAttribute + yearlyWeatherOperator + yearlyWeatherResult

            if self.checkBox_4.isChecked():
                attributeList = attributeList + ","+greenHouseAttribute
                operatorList = " AND "+greenHouseAttribute + greenHouseOperator + greenHouseResult

            if self.checkBox_5.isChecked():
                attributeList = attributeList + ","+airQualityAttribute
                operatorList = " AND "+airQualityAttribute + airQualityOperator + airQualityResult
            """
            if self.checkBox_6.isChecked():
                attributeList = attributeList + ","+waterQualityAttribute
                operatorList = " AND "+waterQualityAttribute + waterQualityOperator + waterQualityResult
            """
            """
            if self.checkBox_7.isChecked():
                attributeList = attributeList + ","+blizzardAttribute
                operatorList = " AND "+blizzardAttribute + blizzardOperator + blizzardResult
            """
            if self.checkBox_8.isChecked():
                attributeList = attributeList + ","+hurricaneAttribute
                operatorList = " AND "+hurricaneAttribute + hurricaneOperator + hurricaneResult

            if self.checkBox_9.isChecked():
                attributeList = attributeList + ","+droughtAttribute
                operatorList = " AND "+droughtAttribute + droughtOperator + droughtResult

            fixedSourceFrom = re.sub('^[,]', '', sourceFrom)
            fixedAttributeList = re.sub('^[,]', '', attributeList)
            fixedOperatorList = re.sub('^[ AND ]+', '', operatorList)

            print(fixedSourceFrom)
            print(fixedOperatorList)

            """edited = '`' + fixedAttributeList + '`'"""
            edited2 = "ORDER BY "+fixedAttributeList+" desc"
            print(edited2)
            sqlCode = "SELECT * FROM "+fixedSourceFrom+" WHERE " + fixedOperatorList +" ORDER BY "+fixedAttributeList+" desc"
            cursor.execute(sqlCode)
            self.progressBar.setValue(80)
            df = pandas.read_sql(sqlCode, cnx)
            self.progressBar.setValue(90)
            model = PandasModel(df)
            self.tableView.setModel(model)
            self.tableView.setBaseSize(1280,400)
            self.tableView.resizeColumnsToContents()
            self.tableView.resizeRowsToContents()
            countOperations = countOperations + 1
            self.lcdNumber.display(countOperations);
            self.progressBar.setValue(100)
        except Exception as e:
            print(e)

    def reset_query(self):
        global countOperations
        global attributeList
        global sourceFrom
        global operatorList
        global attributeList

        countOperations = 0
        attributeList = ""
        operatorList = ""
        sourceFrom = ""
        self.lcdNumber.display(0)
        self.progressBar.setValue(0)


class PandasModel(QtCore.QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
        return None


import Images_rc


if __name__ == "__main__":
    import sys
    import qdarkstyle
    countOperations = 0
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    MainWindow.show()
    sys.exit(app.exec_())
