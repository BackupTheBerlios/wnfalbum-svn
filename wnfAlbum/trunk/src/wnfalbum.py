#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os

__author__="wnf"
__date__ ="$22.11.2009 09:12:33$"

# Must be lower case!
EXT_WHITELIST = (".jpeg", ".png", ".jpg")

class TwnfAlbum:

    def __init__(self,aGrundpfad):
        """initialisiert das Album über den Grundpfad"""
        self.grundpfad = aGrundpfad
        print 'wnfAlbum 0.1'
        print 'Grundpfad: %s' % (self.grundpfad)
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

    def json_jahre(self):
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

if __name__ == "__main__":
    dn = '/wnfdaten/Olympus/'
    a = TwnfAlbum(dn)
    print a.json_jahre()
