#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import ConfigParser
import json
import os
import datetime

__author__="wnf"
__date__ ="$22.11.2009 09:12:33$"

# Must be lower case!
EXT_WHITELIST = (".jpeg", ".png", ".jpg")
SECTION_ALBEN = "Alben"
cMonateL =("Januar","Februar","März","April","Mai","Juni","Juli",
           "August","September","Oktober","November","Dezember")
           
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
            #print self.alben

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

    def get_albumdat_titel(self,v):
        """
        sucht im Verzeichnis nach einer Album.dat Datei und liefert den Titel des Tages
        """
        n=''
        dn='%s/ALBUM.DAT' % (v)
        if os.path.exists(dn):
            ini = ConfigParser.ConfigParser()
            ini.read(dn)
            n=ini.get('TITEL','TITELNAME')
        else:
            dn='%s/Album.dat' % (v)
            if os.path.exists(dn):
                ini = ConfigParser.ConfigParser()
                ini.read(dn)
                n=ini.get('TITEL','TITELNAME')
        n = n.decode("iso-8859-1")
        return n

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
                if i==0:
                    i=d.month
                    monate.append(i)
        return monate

    def album_tage(self,albumnummer,jahr,monat):
        grundpfad=self.album_pfad(albumnummer)
        grundpfad='%s/%d/' % (grundpfad,jahr)
        y = os.listdir(grundpfad)
        y.sort()
        tage = []
        for v in y:
            d = self.verzeichnis_to_date(v)
            if d<>0:
                if monat==d.month:
                    n = self.get_albumdat_titel('%s%s' % (grundpfad,v))
                    n = '%s - %s' % (d.strftime("%d.%m.%Y"),n)
                    tage.append([n,v])
        return tage

    def album_bilder(self,albumnummer,jahr,v):
        grundpfad=self.album_pfad(albumnummer)
        grundpfad='%s/%d/' % (grundpfad,jahr)
        grundpfad='%s%s/' % (grundpfad,v)
        bilder=[]
        for dirpath, dirnames, filenames in os.walk(grundpfad):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                if not os.path.isfile(filepath):
                    continue
                for ext in EXT_WHITELIST:
                    if filename.lower().endswith(ext):
                        bilder.append(filepath)
        bilder.sort()
        return bilder

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
        m=self.album_monate(albumnummer, jahr)
        z = ''
        i = 0
        for s in m:
            if z<>'':
                z = '%s,' % (z)
            z = '%s{"Monat":"%d","Name":"%s"}' % (z,int(s),cMonateL[int(s-1)])
            i=i+1
        z='{"URL":"monat","Params":"Album=%d,Jahr=%d","Monate":[%s]}' % (albumnummer,int(jahr),z)
        return z

    def json_tage(self,albumnummer,jahr,monat):
        m=self.album_tage(albumnummer, jahr,monat)
        z = ''
        i = 0
        for n,v in m:
            if z<>'':
                z = '%s,' % (z)
            z = '%s{"Name":"%s","Verzeichnis":"%s"}' % (z,n,v)
            i=i+1
        z='{"URL":"tage","Params":"Album=%d,Jahr=%d,Monat=%d","Tage":[%s]}' % (albumnummer,int(jahr),int(monat),z)
        return z

    def json_bilder(self,albumnummer,jahr,monat,verzeichnis):
        m=self.album_bilder(albumnummer, jahr,verzeichnis)
        z = ''
        i = 0
        for s in m:
            if z<>'':
                z = '%s,' % (z)
            z = '%s{"Bild":"%s"}' % (z,s)
            i=i+1
        z='{"URL":"bilder","Params":"Album=%d,Jahr=%d,Monat=%d,Tag=%s","Bilder":[%s]}' % (albumnummer,int(jahr),int(monat),verzeichnis,z)
        return z

if __name__ == "__main__":
#   dn = '/wnfdaten/Olympus/'
    a = TwnfAlben()
    print a.json_alben()
    print a.json_jahre(1)
    print a.json_monate(1, 1998)
    print a.json_tage(1, 1998,04)
    print a.json_tage(1, 2009,04)
    print a.json_bilder(1, 2009,04,'2009-04-02')
#   print '{"URL":"album","Params":null,"Alben":[{"Album":0,"Name":"mein"}]}'
#   print a.json_jahre()
#   print a.html_jahre()
