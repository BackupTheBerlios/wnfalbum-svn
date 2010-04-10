#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import ConfigParser
from stat import *
import datetime
import time
import shutil
from PyQt4 import QtGui,QtCore
from wnfkameradownload_am_main import Ui_Dialog as Dlg

class Download_Dlg(QtGui.QDialog, Dlg):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        dn = os.environ["HOME"]
        dn = "%s/.wnfkameradownload" % (dn)
        self.IniPfadname = dn
        dn = "%s/wnfkameradownload.ini" % (dn)
        self.ini=ConfigParser.ConfigParser()
        self.ini.read(dn)
        self.IniDateiname = dn
        self.qpfad=''
        self.zpfad=''
        self.Anzahl=0
        if os.path.exists(dn):
            s = self.lese_str(self.ini,"Standard","Kamera")
            if (s<>''):
                self.ed_Quelle.setText(s)
            s = self.lese_str(self.ini,"Standard","Zielverzeichnis")
            if (s<>''):
                self.ed_Ziel.setText(s)
            s = self.lese_str(self.ini,"Standard","Vorsilbe")
            if (s<>''):
                self.ed_Vorsilbe.setText(s)

    #http://docs.python.org/lib/os-file-dir.html
    def isSchreibrecht(self,aPfad):
        return os.access(aPfad,os.W_OK)

    def isLeserecht(self,aPfad):
        return os.access(aPfad,os.R_OK)

    def ForceDir(self,aPfad):
        if not os.path.exists(aPfad):
            os.makedirs(aPfad)
        return os.path.exists(aPfad)

    def lese_str(self,ini,aSection,aName):
        """" Lesen der Variablen aus der Ini-Datei """
        try:
            s = ini.get(aSection, aName)
        except ConfigParser.NoOptionError:
            s = ""
        return s

    def schreibe_str(self,ini,aSection,aName,aWert):
        """" Schreiben der Variablen in die Ini-Datei """
        if not ini.has_section(aSection):
            ini.add_section(aSection)
        ini.set(aSection, aName,aWert)
        print aWert

    def speicher_ini(self):
        """" Schreiben der Variablen in die Ini-Datei """
        s=self.ed_Quelle.text()
        if (s<>''):
            self.schreibe_str(self.ini,"Standard","Kamera",s)
        s=self.ed_Ziel.text()
        if (s<>''):
            self.schreibe_str(self.ini,"Standard","Zielverzeichnis",s)
        s=self.ed_Vorsilbe.text()
        if (s<>''):
            self.schreibe_str(self.ini,"Standard","Vorsilbe",s)
        self.ForceDir(self.IniPfadname)
        fd = open(self.IniDateiname, 'w')
        self.ini.write(fd)
        fd.close()

    def anzeige(self,s):
        self.me_Status.append(s)
        #Das soll aber gar nicht gut sein:
        #Der Anwendung Zeit geben die Änderung von QTextEdit anzuzeigen
        app.processEvents()
        print s


    def ein_Bild_kopieren(self,dateiname,vorsilbe):
        """ Ein Bild von der Kamera herunterladen,
            wenn es neuer ist oder noch nicht existiert """
        qdn='%s%s' % (self.qpfad,dateiname)
        if os.path.isfile(qdn):
            ctm = os.stat(qdn)[ST_CTIME]
            gmt = time.gmtime(ctm)
            #zp='%s%s/%s England' % (self.zpfad,gmt[0],time.strftime('%Y-%m-%d',gmt))
            zp='%s%s/%s' % (self.zpfad,gmt[0],time.strftime('%Y-%m-%d',gmt))
            if self.ForceDir(zp):
                if self.cx_Rename.isChecked():
                    zdn=vorsilbe #.lower()
                    if zdn<>'':
                        zdn='%s_' % (zdn)
                    zdn='%s%s_' % (zdn,time.strftime('%H_%M_%S',gmt))
                    zdn='%s/%s%s' % (zp,zdn,dateiname.lower())
                else:
                    #hier auf jeden Fall lowercase,
                    #weil nicht sicher ist, wie die Dateinamen
                    #geliefert werden
                    zdn=dateiname.lower()
                    zdn='%s/%s' % (zp,zdn)
                if not os.path.exists(zdn):
                    shutil.copyfile(qdn,zdn)
                    #die Originalzeit wieder setzen
                    os.utime(zdn,(ctm,ctm))
                    self.Anzahl=self.Anzahl+1
                    #self.anzeige('%s -> %s' % (qdn,zdn))
                    self.anzeige('-> %s' % (zdn))

    def download(self, aQuellpfad, aZielpfad):
        """" Herunterladen der Bilder von der Kamera """
        self.qpfad=aQuellpfad
        self.zpfad=aZielpfad
        self.Anzahl=0
        self.anzeige('Das Kamera-Verzeichnis ist: %s' % (self.qpfad))
        self.anzeige('Das Bilder-Verzeichnis ist: %s' % (self.zpfad))
        self.ok=False
        vorsilbe=self.ed_Vorsilbe.text()
        if self.ForceDir(self.zpfad):
            if self.isLeserecht(self.qpfad):
                self.ok=True
            else:
                print "Keine Leserechte vom Verzeichnis %s " % (self.qpfad)
        else:
            print "Keine Schreibrechte auf das Verzeichnis %s " % (self.zpfad)
        if self.ok:
            print 'Download beginnt'
            y = os.listdir(self.qpfad)
            y.sort()
            for dateiname in y:
                self.ein_Bild_kopieren(dateiname,vorsilbe)
            self.anzeige('%d Dateien kopiert.' % (self.Anzahl))
        else:
            self.anzeige('Der Download konnte nicht gestartet werden.')

    @QtCore.pyqtSignature('') # es wird kein Argument entgegen genommen
    def on_bb_Quelle_clicked(self):
        print 'Quellverzeichnis lesen'
        filename = QtGui.QFileDialog.getExistingDirectory(self,
            'Quellverzeichnis waehlen','/media')
        if (filename<>''):
            self.ed_Quelle.setText(filename)
        print filename

    @QtCore.pyqtSignature('') # es wird kein Argument entgegen genommen
    def on_bb_Ziel_clicked(self):
        print 'Zielverzeichnis lesen'
        filename = QtGui.QFileDialog.getExistingDirectory(self,
            'Zielverzeichnis waehlen','/home')
        if (filename<>''):
            self.ed_Ziel.setText(filename)
        print filename

    @QtCore.pyqtSignature('') # es wird kein Argument entgegen genommen
    def on_bb_Laden_clicked(self):
        print 'Herunterladen der Bilder von der Kamera'
        self.speicher_ini()
        self.download(self.ed_Quelle.text(), self.ed_Ziel.text())

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  dialog = Download_Dlg()
  dialog.show()
  sys.exit(app.exec_())
