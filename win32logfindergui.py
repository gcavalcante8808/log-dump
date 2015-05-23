#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gabriel Abdalla Cavalcante Silva'
#
# Done by Gabriel Abdalla Cavalcante Silva
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
# http://www.apache.org/licenses/LICENSE-2.0
from gi.repository import Gtk
import abc


class BaseGui(object):
    """
    A simple Base Class that will contain information needed by all other classes.
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")


class MainWindow(BaseGui):
    """
    The class that holds the main methods for the Main Window of the project, which is used by the Win32LogFinderGui
    class.
    """
    def __init__(self):
        """
        Just Get the Main Window object from the glade file.
        """
        super(MainWindow, self).__init__()
        self.registered_choices = None
        self.mainwindow = self.builder.get_object("MainWindow")

    @abc.abstractmethod
    def on_registered_changed(self, widget):
        """
        This method has some relationship with the RegisteredWindow Class, and will be implemented on the GUI itself,
        not here.
        """
        pass

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


class RegisteredWindow(BaseGui):
    def __init__(self):
        super(RegisteredWindow, self).__init__()
        self.regwindow = self.builder.get_object("RegisteredWindow")

    def on_from_field_choice_changed(self):
        raise NotImplementedError

    def on_from_field_date_insert_at_cursor(self):
        raise NotImplementedError

    def on_from_field_hour_insert_at_cursor(self):
        raise NotImplementedError

    def on_to_field_choice_changed(self):
        raise NotImplementedError

    def on_to_field_date_insert_at_cursor(self):
        raise NotImplementedError

    def on_to_field_hour_insert_at_cursor(self):
        raise NotImplementedError


class Win32LogFinderGui(MainWindow, RegisteredWindow):
    """
    The GUI Itself. This class make some use of all resources presented on all other Classes and provide a high
    level boxing of all GTK resources.
    """
    def __init__(self):
        super(Win32LogFinderGui, self).__init__()

        #Show all Icons in the software.
        settings = Gtk.Settings.get_default()
        settings.props.gtk_button_images = True

        self.builder.connect_signals(self)
        self.mainwindow.connect("delete-event", Gtk.main_quit)
        self.mainwindow.show_all()

    def on_registered_changed(self, widget):
        """
        This method implements the abstract method presented on the MainWindow Class and uses information from
        MainWindow and RegisteredWindow. In fact, if the user chooses the personalized choice, a window appears
        with some options to define de date range of the search.
        :param widget: The ComboBoxTest Registered Choices that comes from the gui.
        :return: None
        """
        active_id = widget.get_active_id()
        if active_id == "anytime":
            raise NotImplementedError
        elif active_id == "personalized":
            self.regwindow.set_transient_for(self.mainwindow)
            self.regwindow.show_all()
        else:
            self.registered_choices = active_id

if __name__ == "__main__":
    window = Win32LogFinderGui()
    Gtk.main()
