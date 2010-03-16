#! /usr/bin/python
# -*- coding: utf-8 -*-

# http://www.rkblog.rk.edu.pl/w/p/qgraphicsview-and-qgraphicsscene/
# 

__author__="wnf"
__date__ ="$08.03.2010 19:55:39$"

import sys
import glob
from PyQt4 import QtCore,QtGui
from wnfalbum_am_main import  Ui_MainWindow


"""
app = QApplication(sys.argv)

grview = QGraphicsView()
scene = QGraphicsScene()
scene.addPixmap(QPixmap('/home/wnf/Bilder/Bernburg_2009/bernburg/bild_0019.jpg'))
grview.setScene(scene)

grview.show()

sys.exit(app.exec_())

if __name__ == "__main__":
    print "Hello World";
"""

class Am_Main(QtGui.QMainWindow, Ui_MainWindow):
    """
    Hauptformular
    """
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.setupUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        self.scene = QtGui.QGraphicsScene()
        self.gv.setScene(self.scene)
        QtCore.QObject.connect(self.actionNextBild, QtCore.SIGNAL("triggered()"), self.nextBildAnzeigen)
        QtCore.QObject.connect(self.actionPrevBild, QtCore.SIGNAL("triggered()"), self.prevBildAnzeigen)

    def einVerzeichnis(self,verzeichnis):
        chain = verzeichnis + "/*"
        self.images = glob.glob(chain)
        self.images.sort(cmp=lambda x, y: cmp(x.lower(), y.lower()))
        """
        self.zoom_step = 0.04
        self.w_vsize = 100 #self.gv.size().width()
        self.h_vsize = 200 #self.gv.size().height()
        if self.w_vsize <= self.h_vsize:
            self.max_vsize = self.w_vsize
        else:
            self.max_vsize = self.h_vsize

        print self.w_vsize,self.h_vsize
        print self.max_vsize,self.max_vsize
        """
        self.l_pix = ["", "", ""]
        self.i_pointer = 0
        self.p_pointer = 0
        self.curBildLaden()
        self.p_pointer = 1
        self.nextBildLaden()
        self.p_pointer = 2
        self.prevBildLaden()
        self.p_pointer = 0

    def curBildLaden(self):
        self.max_hsize = self.width()
        self.max_vsize = self.height()
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[self.i_pointer])
        self.c_view = self.l_pix[self.p_pointer].scaled(self.max_hsize, self.max_vsize,
                                            QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.FastTransformation)
        #change the previous line with QtCore.Qt.SmoothTransformation eventually
        self.curBildAnzeigen()

    def curBildAnzeigen(self):
        size_img = self.c_view.size()
        wth, hgt = QtCore.QSize.width(size_img), QtCore.QSize.height(size_img)
        self.scene.clear()
        self.scene.setSceneRect(0, 0, wth, hgt)
        #self.scene.setSceneRect(0, 0, 100, 200)
        self.scene.addPixmap(self.c_view)
        QtCore.QCoreApplication.processEvents()

    def nextBildAnzeigen(self):
        self.i_pointer += 1
        if self.i_pointer == len(self.images):
            self.i_pointer = 0
        self.p_view = self.c_view
        self.c_view = self.n_view
        self.curBildAnzeigen()
        if self.p_pointer == 0:
            self.p_pointer = 2
            self.nextBildLaden()
            self.p_pointer = 1
        elif self.p_pointer == 1:
            self.p_pointer = 0
            self.nextBildLaden()
            self.p_pointer = 2
        else:
            self.p_pointer = 1
            self.nextBildLaden()
            self.p_pointer = 0

    def nextBildLaden(self):
        if self.i_pointer == len(self.images)-1:
            p = 0
        else:
            p = self.i_pointer + 1
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[p])
        self.n_view = self.l_pix[self.p_pointer].scaled(self.max_vsize,
                                            self.max_vsize,
                                            QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.FastTransformation)
        print self.images[p]

    def prevBildAnzeigen(self):
        self.i_pointer -= 1
        if self.i_pointer <= 0:
            self.i_pointer = len(self.images)-1
        self.n_view = self.c_view
        self.c_view = self.p_view
        self.curBildAnzeigen()
        if self.p_pointer == 0:
            self.p_pointer = 1
            self.prevBildLaden()
            self.p_pointer = 2
        elif self.p_pointer == 1:
            self.p_pointer = 2
            self.prevBildLaden()
            self.p_pointer = 0
        else:
            self.p_pointer = 0
            self.prevBildLaden()
            self.p_pointer = 1

    def prevBildLaden(self):
        if self.i_pointer == 0:
            p = len(self.images)-1
        else:
            p = self.i_pointer - 1
        self.l_pix[self.p_pointer] = QtGui.QPixmap(self.images[p])
        self.p_view = self.l_pix[self.p_pointer].scaled(self.max_vsize,
                                            self.max_vsize,
                                            QtCore.Qt.KeepAspectRatio,
                                            QtCore.Qt.FastTransformation)
        print self.images[p]

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  am = Am_Main()
  am.einVerzeichnis('/home/wnf/Bilder/Bernburg_2009/bernburg');
  am.show()
  sys.exit(app.exec_())