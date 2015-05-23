#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
# http://www.apache.org/licenses/LICENSE-2.0
from gi.repository import Gtk

BOTTOM = Gtk.PositionType.BOTTOM
RIGHT = Gtk.PositionType.RIGHT

class Handler(object):
    def onRegisteredChanged(self, *args):
        print("Registered Changed.")

settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

window = builder.get_object("window1")
window.show_all()
Gtk.main()
