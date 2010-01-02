#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ConfigParser
import json
import os
import datetime
import wnfalbum

__author__="wnf"
__date__ ="$22.11.2009 09:12:33$"

# Must be lower case!
EXT_WHITELIST = (".jpeg", ".png", ".jpg")
SECTION_ALBEN = "Alben"

class TwnfAlbum:

    def __init__(self,aGrundpfad):
        """initialisiert das Album über den Grundpfad"""
        self.grundpfad = aGrundpfad
        print 'wnfAlbum 0.1'
        print 'Grundpfad: %s' % (self.grundpfad)
        #Jahre als Liste ablegen
        self.jahre=[]
        self.tage=[]
        y = os.listdir(self.grundpfad)
        y.sort()
        for aJahr in y:
            p='%s%s/' % (self.grundpfad,aJahr)
            if self.isfotoverzeichnis(self.grundpfad,aJahr):
                self.jahre.append(aJahr)
                print p

    def isint(self,s):
        try:
            int(s)
        except:
            return False
        else:
            return True

    def isfotoverzeichnis(self,v,aJahr):
        if not os.path.isdir(v):
            return False
        if not self.isint(aJahr):
            return False
        return True

    def lese_tage_eines_jahres(self,v):
        self.tage=[]
        y = os.listdir(v)
        y.sort()
        for aTag in y:
            s='%s%s' % (v,aTag)
            if os.path.isdir(s):
                self.tage.append(s)

    def lese_bilder_eines_tages(self,v):
        """
        liefert alle Bilder des Verzeichnisses
        """
        self.bilder=[]
        for dirpath, dirnames, filenames in os.walk(v):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if not os.path.isfile(filepath):
                    continue
                for ext in EXT_WHITELIST:
                    if filename.lower().endswith(ext):
                        self.bilder.append(filepath)
        self.bilder.sort()

    def json_alben(self):
        """ liefert alle Alben als json_object
        {"URL":"album","Params":null,"Alben":[{"Album":0,"Name":"mein"}]}
        """
        z = '{"URL":"album","Params":null,"Alben":['
        z = '%s{"Album":0,"Name":"%s"}' % (z,'Olympus')
        z = '%s]}' % (z)
        return z

    def json_jahre(self):
        """liefert alle Jahre als json_object"""
        z='{"URL":"jahre","Params":"Album=0","Jahre":['
        for i in range(len(self.jahre)):
            z = '%s{"Jahr":"%s"}' % (z,self.jahre[i])
            #einzelne Elemente durch Komma trennen
            if i<len(self.jahre)-1:
                z = '%s,' % (z)
        z = '%s]}' % (z)
        return z

    def json_jahre_x(self):
        """liefert die Jahre des Albums als json_objekt"""
        j=json.loads('["Album", {"Jahr":["baz", null, 1.0, 2]}]')
        return j

    def html_jahre(self):
        """liefert alle Jahre als HTML-Liste"""
        s='<ul>'
        for i in self.jahre:
            s = '%s<li>%s</li>' % (s,i)
        s = '%s</ul>' % (s)
        return s

    def html_letztes_bild(self):
        """liefert letztes Bild als HTML-string"""
        j = self.jahre[len(self.jahre)-1]
        s = '%s/%s/' % (self.grundpfad,j)
        self.lese_tage_eines_jahres(s)
        if len(self.tage)>0:
            j = self.tage[len(self.tage)-1]
            self.lese_bilder_eines_tages(j)
            if len(self.tage)>0:
                j = self.bilder[len(self.bilder)-1]
                s='<ul>'
                s = '%s<li>%s</li>' % (s,j)
                s = '%s</ul>' % (s)
            else:
                s='Kein Bild im Verzeichnis %s' % (s)
        else:
            s='Kein Tag im Verzeichnis %s' % (s)
        return s

class TwnfAlben:

    def __init__(self):
        """
        liefert den Namen der ini-Datei
        """
        ini_dn = os.environ["HOME"]
        ini_dn = "%s/.wlsoft/wnfAlbum.ini" % (ini_dn)
        print ini_dn
        self.alben = ()
        if os.path.exists(ini_dn):
            ini = ConfigParser.ConfigParser()
            ini.read(ini_dn)
            self.alben = ini.items(SECTION_ALBEN)
            self.alben.sort()
            print self.alben

    def isint(self,s):
        try:
            int(s)
        except:
            return False
        else:
            return True

    def get_date(self,jjjj,mm,tt):
        try:
            d = datetime.date(int(jjjj),int(mm),int(tt))
        except:
            d = 0
        return d

    def isfotoverzeichnis(self,v,aJahr):
        if not os.path.isdir(v):
            return False
        if not self.isint(aJahr):
            return False
        return True
    
    def verzeichnis_to_date(self,v):
        """
        wandelt das Verzeichnis in ein Datum (wenn möglich)
        """
        #2009-12-31
        jjjj = v[0:4]
        mm = v[5:7]
        tt = v[8:10]
        #print jjjj,mm,tt
        d=self.get_date(jjjj,mm,tt)
        if d==0:
            #20091231
            jjjj = v[0:4]
            mm = v[4:6]
            tt = v[6:8]
            d=self.get_date(jjjj,mm,tt)
        if d==0:
            #09-12-31
            jjjj = v[0:2]
            mm = v[2:4]
            tt = v[4:6]
            if jjjj<'20':
                jjjj = "20%s" % (jjjj)
            else:
                jjjj = "19%s" % (jjjj)
            d=self.get_date(jjjj,mm,tt)
        #if d<>0:
        #    print jjjj,mm,tt
        return d

    def album_pfad(self,albumnummer):
        p = ''
        if albumnummer<len(self.alben):
            n,p = self.alben[albumnummer]
        return p

    def album_jahre(self,albumnummer):
        grundpfad=self.album_pfad(albumnummer)
        y = os.listdir(grundpfad)
        y.sort()
        jahre = []
        for aJahr in y:
            p='%s/%s/' % (grundpfad,aJahr)
            if self.isfotoverzeichnis(grundpfad,aJahr):
                jahre.append(aJahr)
                #print p
        return jahre

    def album_monate(self,albumnummer,jahr):
        grundpfad=self.album_pfad(albumnummer)
        grundpfad='%s/%d/' % (grundpfad,jahr)
        y = os.listdir(grundpfad)
        y.sort()
        monate = []
        for v in y:
            d = self.verzeichnis_to_date(v)
            if d<>0:
                i=0
                for i in monate:
                    if i==d.month:
                        break
                    else:
                        i=0
                print i,d.month
                if i==0:
                    i=d.month
                    print i,v,d
                    monate.append(i)
        return monate

    def json_alben(self):
        z = ''
        i = 0
        for n,p in self.alben:
            if z<>'':
                z = '%s,' % (z)
            z = '%s{"Album":%d,"Name":"%s"}' % (z,i,n)
            i=i+1
        z = '{"URL":"album","Params":null,"Alben":[%s]}' % (z)
        return z

    def json_jahre(self,albumnummer):
        p=self.album_jahre(albumnummer)
        z = ''
        i = 0
        for s in p:
            if z<>'':
                z = '%s,' % (z)
            z = '%s{"Jahr":"%s"}' % (z,s)
            i=i+1
        z='{"URL":"jahre","Params":"Album=%d","Jahre":[%s]}' % (albumnummer,z)
        return z

    def json_monate(self,albumnummer,jahr):
        z = self.album_monate(albumnummer, jahr)
        return z

if __name__ == "__main__":
#   dn = '/wnfdaten/Olympus/'
    a = TwnfAlben()
    print a.json_alben()
    print a.json_jahre(1)
    print a.json_monate(1, 2000)
#   print '{"URL":"album","Params":null,"Alben":[{"Album":0,"Name":"mein"}]}'
#   print a.json_jahre()
#   print a.html_jahre()
