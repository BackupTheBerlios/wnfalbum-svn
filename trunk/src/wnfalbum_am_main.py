# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wnfalbum_am_main.ui'
#
# Created: Mon Nov 22 17:57:51 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cb_jahre = KComboBox(self.centralwidget)
        self.cb_jahre.setMinimumSize(QtCore.QSize(120, 0))
        self.cb_jahre.setMaximumSize(QtCore.QSize(120, 16777215))
        self.cb_jahre.setObjectName("cb_jahre")
        self.horizontalLayout.addWidget(self.cb_jahre)
        self.cb_tage = KComboBox(self.centralwidget)
        self.cb_tage.setObjectName("cb_tage")
        self.horizontalLayout.addWidget(self.cb_tage)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gv = QtGui.QGraphicsView(self.centralwidget)
        self.gv.setObjectName("gv")
        self.verticalLayout.addWidget(self.gv)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuBild = QtGui.QMenu(self.menubar)
        self.menuBild.setObjectName("menuBild")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionNextBild = QtGui.QAction(MainWindow)
        self.actionNextBild.setObjectName("actionNextBild")
        self.actionPrevBild = QtGui.QAction(MainWindow)
        self.actionPrevBild.setObjectName("actionPrevBild")
        self.actionDiashow = QtGui.QAction(MainWindow)
        self.actionDiashow.setObjectName("actionDiashow")
        self.menuBild.addAction(self.actionNextBild)
        self.menuBild.addAction(self.actionPrevBild)
        self.menuBild.addAction(self.actionDiashow)
        self.menubar.addAction(self.menuBild.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuBild.setTitle(QtGui.QApplication.translate("MainWindow", "Bild", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNextBild.setText(QtGui.QApplication.translate("MainWindow", "ein Bild vor", None, QtGui.QApplication.UnicodeUTF8))
        self.actionNextBild.setShortcut(QtGui.QApplication.translate("MainWindow", "Space", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrevBild.setText(QtGui.QApplication.translate("MainWindow", "ein Bild zurück", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPrevBild.setShortcut(QtGui.QApplication.translate("MainWindow", "Backspace", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDiashow.setText(QtGui.QApplication.translate("MainWindow", "Diashow", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDiashow.setToolTip(QtGui.QApplication.translate("MainWindow", "Diashow starten", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDiashow.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))

from PyKDE4.kdeui import KComboBox
