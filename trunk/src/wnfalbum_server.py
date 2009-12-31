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
        print id,args,kwargs
        if id=='album':
            z = self.album(*args)
        elif id=='jahre':
            z = self.jahre(*args)
        elif id=='monat':
            z = self.monat(*args)
        elif id=='tage':
            z = self.tage(*args)
        elif id=='bilder':
            z = self.bilder(*args)
        else:
            z = "Unbekannter Ausdruck: %s" % (id)
        return z
    q.exposed = True

    def default(self,*args, **kwargs):
        e = """
            Hierher gelangen Sie, wenn Sie sich vertippt haben
            Methode default() der Klasse Start.
            Argumente:%s""" % str(args)
        return e
    default.exposed = True

    def album (self, *args):
        z = '{"URL":"album","Params":null,"Alben":['
        z = '%s{"Album":0,"Name":"%s"},' % (z,'Olympus')
        z = '%s{"Album":0,"Name":"%s"}' % (z,'Ixus')
        z = '%s]}' % (z)
        return z
    album.exposed = True

    def jahre (self,*args):
        z='{"URL":"jahre","Params":"Album=0","Jahre":['
        for i in range(10):
            z = '%s{"Jahr":"%d"}' % (z,i+2000)
            #einzelne Elemente durch Komma trennen
            if i<10-1:
                z = '%s,' % (z)
        z = '%s]}' % (z)
        return z
    jahre.exposed = True

    def monat (self,*args):
        z="""{"URL":"monat","Params":"Album=0,Jahr=2009","Monate":[
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
        return z

    def tage (self,*args):
        z="""{"URL":"tage","Params":"Album=0,Jahr=2009,Monat=12","Tage":[
        {"Name":"07 - ","Verzeichnis":"20091207"},
        {"Name":"09 - ","Verzeichnis":"20091209"},
        {"Name":"24 - Weihnachten","Verzeichnis":"20091224"},
        {"Name":"24 - Ralf",
        "Verzeichnis":"20091224 Ralf"}
        ]}"""
        return z

    def bilder (self,*args):
        z="""{"URL":"bilder","Params":"Album=0,Jahr=2009,Monat=12,Tag=20091207",
        "Bilder":[
        {"Bild":"Hund Ralf.JPG"},
        {"Bild":"uwe.jpg"}
        ]}"""
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
