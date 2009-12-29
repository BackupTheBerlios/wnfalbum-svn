#! /usr/bin/python
# -*- coding: utf-8 -*-

# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="wnf"
__date__ ="$29.12.2009 09:34:02$"

import cherrypy

def get_html(aCaption):
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
    m = """
            <ul>
            <li><a href="/">Home</a></li>
            <li><a href="/wnfalbum">wnfAlbum</a></li>
            <li><a href="/wnfjahre">wnfJahre</a></li>
            </ul>
            """
    s = s.replace('_MENU_',m)
    s = s.replace('_TITEL_',aCaption)
    s = s.replace('_CAPTION_',aCaption)
    s = s.replace('_CONTENT_',aCaption)
    return s


class Root:
    def index(self,*args):
        s = get_html('Root')
        return s
    index.exposed = True

    def wnfalbum(self,*args):
        s = get_html('wnfAlbum')
        return s
    wnfalbum.exposed = True

    def wnfjahre(self,*args):
        s = get_html('wnfJahre')
        return s
    wnfjahre.exposed = True

if __name__ == "__main__":
    print "Hello World";
    #Aufbauen der Anwendung
    #Starten des Servers
    #cherrypy.server.start()
    cherrypy.quickstart(Root())
