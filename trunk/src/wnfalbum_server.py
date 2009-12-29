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
"""

import os
import sys
import cherrypy
import time
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

    def q(self,*args):
        print(args)
        if args[0]=='album':
            z = self.album()
        elif args[0]=='jahre':
            z = self.jahre()
        else:
            z = ''
        return z
    q.exposed = True

    def album (self):
        z = '{"URL":"album","Params":null,"Alben":['
        z = '%s{"Album":0,"Name":"%s"}' % (z,'Olympus')
        z = '%s]}' % (z)
        return z
    album.exposed = True

    def jahre (self):
        z = '{"URL":"album","Params":null,"Alben":['
        z = '%s{"Album":0,"Name":"%s"}' % (z,'Olympus')
        z = '%s]}' % (z)
        return z
    jahre.exposed = True
    
    def default(self,*args):
        e = """
            Hierher gelangen Sie, wenn Sie sich vertippt haben
            Methode default() der Klasse Start.
            Argumente:%s""" % str(args)
        return e
    default.exposed = True

class q(object):
    def album (self):
        z = '{"URL":"album","Params":null,"Alben":['
        z = '%s{"Album":0,"Name":"%s"}' % (z,'Olympus')
        z = '%s]}' % (z)
        return z
    album.exposed = True


def main_alt():
    app = cherrypy.tree.mount(Root(), config = INI_FILENAME)
    cherrypy.config.update({"tools.staticdir.root": APPDIR})
    cherrypy.quickstart(app)

def main():
    app = cherrypy.tree.mount(Root(), config = INI_FILENAME)
    cherrypy.config.update({"tools.staticdir.root": APPDIR})
    #Aufbauen der Anwendung
    cherrypy.root = Root()
    cherrypy.root.q = q()
    #Starten des Servers
    cherrypy.quickstart(app)

if __name__ == "__main__":
    main()
