#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import json
import os

__author__="wnf"
__date__ ="$22.11.2009 09:12:33$"

class TwnfAlbum:

    def __init__(self,aGrundpfad):
        """initialisiert das Album über den Grundpfad"""
        self.grundpfad = aGrundpfad
        print 'wnfAlbum 0.1'
        print 'Grundpfad: %s' % (self.grundpfad)
        s=''
        y = os.listdir(self.grundpfad)
        y.sort()
        for aJahr in y:
            p='%s%s/' % (self.grundpfad,aJahr)
            if self.isFotoVerzeichnis(self.grundpfad,aJahr):
                print p

    def isint(self,s):
        try:
            int(s)
        except:
            return False
        else:
            return True

    def isFotoVerzeichnis(self,v,aJahr):
        if not os.path.isdir(v):
            return False
        if not self.isint(aJahr):
            return False
        return True

    def json_jahre(self):
        """liefert die Jahre des Albums als json_objekt"""
        j=json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
        return j


if __name__ == "__main__":
    dn = '/wnfdaten/Olympus/'
    a = TwnfAlbum(dn)
    print a.json_jahre()
