#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import sys
import os
import os.path
import ConfigParser
from stat import *
import datetime
from datetime import timedelta
import time
import shutil
from PyQt4 import QtGui,QtCore
from wnfkameradownload_am_main import Ui_Dialog as Dlg

class Download_Dlg(QtGui.QDialog, Dlg):
    def __init__(self,args):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowTitle('wnfKameraDownload 1.04')
        dn=self.paramStr(args,1)
        if dn=="":
            #oder es wird das Standard Ini-File verwendet
            dn = os.environ["HOME"]
            dn = "%s/.wnfkameradownload" % (dn)
            self.IniPfadname = dn
            dn = "%s/wnfkameradownload.ini" % (dn)
        else:
            self.IniPfadname = os.path.dirname(dn)
        print "Auswerten von ",dn

        self.ini=ConfigParser.ConfigParser()
        self.ini.read(dn)
        self.IniDateiname = dn
        self.qpfad=''
        self.zpfad=''
        self.vorsilbe=''
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
            b = self.lese_bool(self.ini,"Standard","Rename")
            self.cx_Rename.setChecked(b)
            b = self.lese_bool(self.ini,"Standard","Rotate")
            self.cx_Rotate.setChecked(b)
            b = self.lese_bool(self.ini,"Standard","Silvestermodus")
            self.cx_Silvestermodus.setChecked(b)

    def paramStr(self,args,ipos):
        s=""
        i=0
        for a in args:
            if i==ipos:
                s=a
                break
            i=i+1
        return s

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

    def lese_bool(self,ini,aSection,aName):
        s=self.lese_str(ini, aSection, aName)
        return s.lower() in ["yes", "true", "t", "ja","j"]

    def schreibe_bool(self,ini,aSection,aName,aWert):
        if aWert:
            s='ja'
        else:
            s='nein'
        self.schreibe_str(ini, aSection, aName, s)

    def speicher_ini(self):
        """" Schreiben der Variablen in die Ini-Datei """
        s=self.ed_Quelle.text()
        if (s<>''):
            self.schreibe_str(self.ini,"Standard","Kamera",s)
        s=self.ed_Ziel.text()
        if (s<>''):
            self.schreibe_str(self.ini,"Standard","Zielverzeichnis",s)
        s=self.ed_Vorsilbe.text()
        self.schreibe_str(self.ini,"Standard","Vorsilbe",s)
        b=self.cx_Rename.isChecked()
        self.schreibe_bool(self.ini,"Standard","Rename",b)
        b=self.cx_Rotate.isChecked()
        self.schreibe_bool(self.ini,"Standard","Rotate",b)
        b=self.cx_Silvestermodus.isChecked()
        self.schreibe_bool(self.ini,"Standard","Silvestermodus",b)
        #
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

    def ein_Bild_kopieren(self,dirname,dateiname,vorsilbe):
        """ Ein Bild von der Kamera herunterladen,
            wenn es neuer ist oder noch nicht existiert """
        #qdn='%s%s' % (self.qpfad,dateiname)
        qdn=os.path.join(dirname, dateiname)
        if os.path.isfile(qdn):
            ctm = os.stat(qdn)[ST_CTIME]
            ctm = ctm + 60*60
            gmt = time.gmtime(ctm)
            #gmt = time.localtime(ctm) Das bringt schwierigkeiten wenn bilder vor der Sommerteit aufgenommen und da
            if (self.cx_Silvestermodus.isChecked() and gmt[3]<3):
                ctm_vortag = ctm - (24*60*60)
                gmt_vortag = time.gmtime(ctm_vortag)
                #print "Silvester",gmt
                zp=os.path.join(self.zpfad,str(gmt_vortag[0]))
                zp=os.path.join(zp,time.strftime('%Y-%m-%d',gmt_vortag))
            else:
                zp=os.path.join(self.zpfad,str(gmt[0]))
                zp=os.path.join(zp,time.strftime('%Y-%m-%d',gmt))
            #print zp
            if self.ForceDir(zp):
                if self.cx_Rename.isChecked():
                    zdn=vorsilbe.lower()
                    if zdn<>'':
                        zdn='%s_' % (zdn)
                    zdn='%s%s_' % (zdn,time.strftime('%Y_%m_%d_%H_%M_%S',gmt))
                    zdn='%s%s' % (zdn,dateiname.lower())
                    zdn=os.path.join(zp, zdn)
                else:
                    #hier auf jeden Fall lowercase,
                    #weil nicht sicher ist, wie die Dateinamen
                    #geliefert werden
                    zdn=dateiname.lower()
                    zdn=os.path.join(zp, zdn)
                if not os.path.exists(zdn):
                    shutil.copyfile(qdn,zdn)
                    #die Originalzeit wieder setzen
                    os.utime(zdn,(ctm,ctm))
                    self.Anzahl=self.Anzahl+1
                    if self.cx_Rotate.isChecked():
                        #Jetzt das Bild rotieren, falls möglich und nötig
                        os.system('exifautotran %s' % (zdn))
                    #self.anzeige('%s -> %s' % (qdn,zdn))
                    #print gmt
                    self.anzeige('-> %s' % (zdn))

    def download_ein_Verzeichnis(self,data,dirname,filesindir):
        #print (dirname)
        for dateiname in filesindir:
            #print (dateiname)
            self.ein_Bild_kopieren(dirname,dateiname,self.vorsilbe)
 
    def download(self, aQuellpfad, aZielpfad):
        """" Herunterladen der Bilder von der Kamera """
        self.qpfad=aQuellpfad
        self.zpfad=aZielpfad
        self.Anzahl=0
        self.anzeige('Das Kamera-Verzeichnis ist: %s' % (self.qpfad))
        self.anzeige('Das Bilder-Verzeichnis ist: %s' % (self.zpfad))
        self.ok=False
        self.vorsilbe=str(self.ed_Vorsilbe.text())
        if self.ForceDir(self.zpfad):
            if self.isLeserecht(self.qpfad):
                self.ok=True
            else:
                s="Keine Leserechte vom Verzeichnis %s " % (self.qpfad)
                print s
                self.anzeige(s)
        else:
            print "Keine Schreibrechte auf das Verzeichnis %s " % (self.zpfad)
        if self.ok:
            print 'Download beginnt'
            os.path.walk(self.qpfad,self.download_ein_Verzeichnis,None)
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
        self.download(str(self.ed_Quelle.text()), str(self.ed_Ziel.text()))

if __name__ == '__main__':
  app = QtGui.QApplication(sys.argv)
  dialog = Download_Dlg(sys.argv)
  dialog.show()
  sys.exit(app.exec_())
