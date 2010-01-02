#! /usr/bin/python
# -*- coding: utf-8 -*-

__author__="wnf"
__date__ ="$29.12.2009 06:38:52$"

"""
Requirements
    - Python: http://www.python.org/
    - cherrypy: http://cherrypy.org/
    - cheetah: http://www.cheetahtemplate.org/
Literatur:
http://archiv.tu-chemnitz.de/pub/2007/0048/data/Studienarbeit_Ajax_AndreLanger.pdf
http://www.fh-wedel.de/~si/seminare/ws06/Ausarbeitung/09.Python/python3.htm
http://www.cherrypy.org/wiki/CherryPyFaq
"""

import os
import cherrypy
from Cheetah.Template import Template
import wnfalbum


THISDIR = APPDIR = os.path.dirname(os.path.abspath(__file__))
INI_FILENAME = os.path.join(THISDIR, "wnfalbum_server.ini")
WWWDIR = os.path.join(os.path.join(THISDIR, ".."),"www")
INDEX_FILENAME = os.path.join(WWWDIR, "index.html")


class Root(object):

    def index(self, *args, **kwargs):
        """
        Handler für die Startseite
        """
        template = Template(file = os.path.join(WWWDIR, "index.html"))
        return unicode(template)
    index.exposed = True

    def q(self, id, *args, **kwargs):
        #print kwargs
        if id=='album':
            z = self.album()
        elif id=='jahre':
            albumnummer = int(kwargs['Album'])
            z = self.jahre(albumnummer)
        elif id=='monat':
            albumnummer = int(kwargs['Album'])
            jahr = int(kwargs['Jahr'])
            z = self.monat(albumnummer,jahr)
        elif id=='tage':
            albumnummer = int(kwargs['Album'])
            jahr = int(kwargs['Jahr'])
            monat = int(kwargs['Monat'])
            z = self.tage(albumnummer,jahr,monat)
        elif id=='bilder':
            albumnummer = int(kwargs['Album'])
            jahr = int(kwargs['Jahr'])
            monat = int(kwargs['Monat'])
            verzeichnis = kwargs['Tag']
            z = self.bilder(albumnummer,jahr,monat,verzeichnis)
        else:
            print id,kwargs
            print "Unbekannter Ausdruck: %s " % (id)
            z = ""
        return z
    q.exposed = True

    def default(self,*args, **kwargs):
        e = """
            Hierher gelangen Sie, wenn Sie sich vertippt haben
            Methode default() der Klasse Start.
            Argumente:%s""" % str(args)
        return e
    default.exposed = True

    def album (self):
        a = wnfalbum.TwnfAlben()
        z = a.json_alben()
        return z

    def jahre (self,albumnummer):
        """
        {"URL":"jahre","Params":"Album=0","Jahre":['
        """
        a = wnfalbum.TwnfAlben()
        z = a.json_jahre(albumnummer)
        return z

    def monat (self,albumnummer,jahr):
        """
          {"URL":"monat","Params":"Album=0,Jahr=2009","Monate":[
          {"Monat":1,"Name":"Januar"},
          {"Monat":2,"Name":"Februar"},
          {"Monat":3,"Name":"März"},
          {"Monat":4,"Name":"April"},
          {"Monat":5,"Name":"Mai"},
          {"Monat":6,"Name":"Juni"},
          {"Monat":7,"Name":"Juli"},
          {"Monat":8,"Name":"August"},
          {"Monat":9,"Name":"September"},
          {"Monat":10,"Name":"Oktober"},
          {"Monat":11,"Name":"November"},
          {"Monat":12,"Name":"Dezember"}]}
          """
        a = wnfalbum.TwnfAlben()
        z = a.json_monate(albumnummer, jahr)
        return z

    def tage (self,albumnummer,jahr,monat):
        """{"URL":"tage","Params":"Album=0,Jahr=2009,Monat=12","Tage":[
        {"Name":"07 - ","Verzeichnis":"20091207"},
        {"Name":"09 - ","Verzeichnis":"20091209"},
        {"Name":"24 - Weihnachten","Verzeichnis":"20091224"},
        {"Name":"24 - Ralf","Verzeichnis":"20091224 Ralf"}
        ]}
        """
        a = wnfalbum.TwnfAlben()
        z = a.json_tage(albumnummer, jahr, monat)
        return z

    def bilder (self,albumnummer,jahr,monat,verzeichnis):
        """
        {"URL":"bilder","Params":"Album=0,Jahr=2009,Monat=12,Tag=20091207",
        "Bilder":[
        {"Bild":"Hund Ralf.JPG"},
        {"Bild":"uwe.jpg"}
        ]}
        """
        a = wnfalbum.TwnfAlben()
        z = a.json_bilder(albumnummer, jahr, monat, verzeichnis)
        return z

def main():
    app = cherrypy.tree.mount(Root(), config = INI_FILENAME)
    cherrypy.config.update({"tools.staticdir.root": APPDIR})
    #Aufbauen der Anwendung
    cherrypy.root = Root()
    #Starten des Servers
    cherrypy.quickstart(app)

if __name__ == "__main__":
    main()
