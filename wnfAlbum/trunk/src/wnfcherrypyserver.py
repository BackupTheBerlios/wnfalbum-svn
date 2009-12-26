#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__="wnf"
__date__ ="$23.11.2009 14:01:50$"

import cherrypy
import wnfalbum

class StartSeite(object):

    def __init__(self, aGrundpfad):
        self.Progversion = '0.01'
        self.Progname = 'wnfAlbum %s' % self.Progversion
        self.Album = wnfalbum.TwnfAlbum(aGrundpfad)
        print self.Progname

    @cherrypy.expose
    def index(self):
        s = self.get_html()
        s = s.replace('_CAPTION_',"Meine Bilder")
        jahre = self.Album.html_jahre()
        letztes_bild = self.Album.html_letztes_bild()
        s = s.replace('_MENU_',jahre)
        s = s.replace('_CONTENT_',letztes_bild)
        return s

    def get_html(self):
        s = """
            <html>
            <head>
            <title>_TITEL_</title>
            </head>
            <body>
            <h1>_CAPTION_</h1>
            <h2>Men&uuml;</h2>
            <p>
            _MENU_
            </p>
            <p>
            _CONTENT_
            </p>
            </body>
            </html>
            """
        s = s.replace('_TITEL_',self.Progname)
        return s
        
import os.path
wnfconf = os.path.join(os.path.dirname(__file__), 'wnfcherryserver.conf')
print wnfconf
aGrundpfad='/wnfdaten/Olympus'
cherrypy.quickstart(StartSeite(aGrundpfad), '/', config=wnfconf)
