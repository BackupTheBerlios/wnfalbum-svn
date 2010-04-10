# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'wnfkameradownload_am_main.ui'
#
# Created: Sat Apr 10 17:22:30 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(514, 354)
        Dialog.setSizeGripEnabled(True)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(6, 17, 501, 151))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridlayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridlayout.setObjectName("gridlayout")
        self.ed_Quelle = QtGui.QLineEdit(self.layoutWidget)
        self.ed_Quelle.setObjectName("ed_Quelle")
        self.gridlayout.addWidget(self.ed_Quelle, 0, 0, 1, 1)
        self.bb_Quelle = QtGui.QPushButton(self.layoutWidget)
        self.bb_Quelle.setObjectName("bb_Quelle")
        self.gridlayout.addWidget(self.bb_Quelle, 0, 1, 1, 1)
        self.ed_Ziel = QtGui.QLineEdit(self.layoutWidget)
        self.ed_Ziel.setObjectName("ed_Ziel")
        self.gridlayout.addWidget(self.ed_Ziel, 1, 0, 1, 1)
        self.bb_Ziel = QtGui.QPushButton(self.layoutWidget)
        self.bb_Ziel.setObjectName("bb_Ziel")
        self.gridlayout.addWidget(self.bb_Ziel, 1, 1, 1, 1)
        self.bb_Laden = QtGui.QPushButton(self.layoutWidget)
        self.bb_Laden.setObjectName("bb_Laden")
        self.gridlayout.addWidget(self.bb_Laden, 2, 1, 1, 1)
        self.cx_Rename = QtGui.QCheckBox(self.layoutWidget)
        self.cx_Rename.setChecked(True)
        self.cx_Rename.setObjectName("cx_Rename")
        self.gridlayout.addWidget(self.cx_Rename, 2, 0, 1, 1)
        self.ed_Vorsilbe = QtGui.QLineEdit(self.layoutWidget)
        self.ed_Vorsilbe.setObjectName("ed_Vorsilbe")
        self.gridlayout.addWidget(self.ed_Vorsilbe, 3, 0, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 3, 1, 1, 1)
        self.me_Status = QtGui.QTextEdit(Dialog)
        self.me_Status.setGeometry(QtCore.QRect(8, 180, 501, 151))
        self.me_Status.setObjectName("me_Status")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Kamera Download", None, QtGui.QApplication.UnicodeUTF8))
        self.bb_Quelle.setText(QtGui.QApplication.translate("Dialog", "Kamera wählen", None, QtGui.QApplication.UnicodeUTF8))
        self.bb_Ziel.setText(QtGui.QApplication.translate("Dialog", "Bilderverzeichnis", None, QtGui.QApplication.UnicodeUTF8))
        self.bb_Laden.setText(QtGui.QApplication.translate("Dialog", "Herunterladen", None, QtGui.QApplication.UnicodeUTF8))
        self.cx_Rename.setToolTip(QtGui.QApplication.translate("Dialog", "Falls im Urlaub mit mehreren Kameras fotografiert wurde, kann man durch das Umbenennen erreichen, dass die Bilder in der richtigen zeitlichen Reihenfolge angezeigt werden. Umbenannt wird nach\n"
"Vorsilbe_JJJJ_MM_TT_HH_MM_SS.jpg", None, QtGui.QApplication.UnicodeUTF8))
        self.cx_Rename.setText(QtGui.QApplication.translate("Dialog", "Die Bilder beim herunterladen umbenennen", None, QtGui.QApplication.UnicodeUTF8))
        self.ed_Vorsilbe.setToolTip(QtGui.QApplication.translate("Dialog", "Entweder eine Vorsilbe für das Umbenennen eingeben (oder leer lassen, wenn nicht umbenannt werden soll)", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Vorsilbe eintragen", None, QtGui.QApplication.UnicodeUTF8))

