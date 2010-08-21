#!/usr/bin/python
# -*- coding: utf-8 -*-

import gtk

class Tabelle1(object):

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Mein erstes Fenster")
        self.window.set_default_size(800, 600)
        self.window.maximize()
        self.window.connect("delete_event", self.event_delete)
        self.window.connect("destroy", self.destroy)
        table = gtk.Table(3, 2, False)
        self.window.add(table)
        label = gtk.Label("Zelle 1-1")
        table.attach(label, 0, 1, 0, 1)
        label.show()
        label = gtk.Label("Zelle 1-2")
        table.attach(label, 1, 2, 0, 1)
        label.show()
        label = gtk.Label("Eine etwas größere Zelle")
        table.attach(label, 0, 1, 1, 2)
        label.show()
        label = gtk.Label("Zelle 2-2")
        table.attach(label, 1, 2, 1, 2)
        label.show()
        label = gtk.Label("<u>die letzte Zeile geht über die gesamte Tabellenbreite</u>")
        label.set_use_markup(True)
        table.attach(label, 0, 2, 2, 3)
        label.show()
        table.show()
        self.window.show()
        print 'init beendet.'

    def event_delete(self, widget, event, data=None):
        return False

    def destroy(self, data=None):
        gtk.main_quit()

    def draw_pixmap(self, x, y):
        pixmap, mask = gtk.gdk.pixmap_create_from_xpm(
        self.area.window, self.style.bg[gtk.STATE_NORMAL], "gtk.xpm")
        self.area.window.draw_drawable(self.gc, pixmap, 0, 0, x+15, y+25,-1, -1)
        self.pangolayout.set_text("Pixmap")
        self.area.window.draw_layout(self.gc, x+5, y+80, self.pangolayout)
        return

    def main(self):
        gtk.main()
        #self.draw_pixmap(100, 200)


if __name__ == "__main__":
    tab = Tabelle1()
    tab.main()