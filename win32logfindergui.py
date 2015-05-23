#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gabriel Abdalla Cavalcante Silva'
#
# Done by Gabriel Abdalla Cavalcante Silva
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
# http://www.apache.org/licenses/LICENSE-2.0
from gi.repository import Gtk


class Handler(object):
    def on_registered_changed(self, *args):
        raise NotImplementedError

    def on_delete_window(self, *args):
        Gtk.main_quit()

    def on_search_clicked(self, *args):
        raise NotImplementedError

    def on_clear_clicked(self, *args):
        raise NotImplementedError

    def on_about_activated(self, *args):
        raise NotImplementedError

    def on_search_order_cb_changed(self, *args):
        raise NotImplementedError

settings = Gtk.Settings.get_default()
settings.props.gtk_button_images = True

builder = Gtk.Builder()
builder.add_from_file("gui.glade")
builder.connect_signals(Handler())

window = builder.get_object("MainWindow")
window.show_all()
Gtk.main()
