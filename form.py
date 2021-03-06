# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_photo = QtWidgets.QLabel(self.centralwidget)
        self.label_photo.setGeometry(QtCore.QRect(100, 20, 600, 450))
        self.label_photo.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.label_photo.setAlignment(QtCore.Qt.AlignCenter)
        self.label_photo.setObjectName("label_photo")
        self.search_line = QtWidgets.QLineEdit(self.centralwidget)
        self.search_line.setGeometry(QtCore.QRect(10, 480, 580, 40))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.search_line.setFont(font)
        self.search_line.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.search_line.setText("")
        self.search_line.setObjectName("search_line")
        self.search_btn = QtWidgets.QPushButton(self.centralwidget)
        self.search_btn.setGeometry(QtCore.QRect(590, 480, 81, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.search_btn.setFont(font)
        self.search_btn.setObjectName("search_btn")
        self.clear_btn = QtWidgets.QPushButton(self.centralwidget)
        self.clear_btn.setGeometry(QtCore.QRect(670, 480, 61, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.clear_btn.setFont(font)
        self.clear_btn.setObjectName("clear_btn")
        self.address_label = QtWidgets.QLabel(self.centralwidget)
        self.address_label.setGeometry(QtCore.QRect(10, 540, 791, 81))
        font = QtGui.QFont()
        font.setPointSize(13)
        self.address_label.setFont(font)
        self.address_label.setText("")
        self.address_label.setObjectName("address_label")
        self.postal_code_checkbox = QtWidgets.QCheckBox(self.centralwidget)
        self.postal_code_checkbox.setGeometry(QtCore.QRect(660, 570, 131, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.postal_code_checkbox.setFont(font)
        self.postal_code_checkbox.setObjectName("postal_code_checkbox")
        self.type_btn = QtWidgets.QPushButton(self.centralwidget)
        self.type_btn.setGeometry(QtCore.QRect(630, 430, 70, 40))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.type_btn.setFont(font)
        self.type_btn.setObjectName("type_btn")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_photo.setText(_translate("MainWindow", "TextLabel"))
        self.search_btn.setText(_translate("MainWindow", "Search"))
        self.clear_btn.setText(_translate("MainWindow", "Clear"))
        self.postal_code_checkbox.setText(_translate("MainWindow", "Show index"))
        self.type_btn.setText(_translate("MainWindow", "Type"))
