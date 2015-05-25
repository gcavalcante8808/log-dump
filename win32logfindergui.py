#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = 'Gabriel Abdalla Cavalcante Silva'
#
# Done by Gabriel Abdalla Cavalcante Silva
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
# http://www.apache.org/licenses/LICENSE-2.0
from gi.repository import Gtk
from ui.register import RegisteredWindow, Register
from ui.main import MainWindow


class Win32LogFinderGui(MainWindow, RegisteredWindow):
    """
    The GUI Itself. This class make some use of all resources presented on all
    other Classes and provide a high level boxing of all GTK resources.
    """

    def __init__(self):
        super(Win32LogFinderGui, self).__init__()

        # Show all Icons in the software.
        settings = Gtk.Settings.get_default()
        settings.props.gtk_button_images = True

        self.builder.connect_signals(self)
        self.mainwindow.connect("delete-event", Gtk.main_quit)
        self.mainwindow.show_all()

    def _object_picker(self, widget_name):
        """
        Get the instance based on a widget_name passed.
        :param widget_name: The name of the widget got from widget.get_name().
        :return: A list with all instances that matches the string search.
        """
        obj = [obj for obj in Register.instances if obj.name in widget_name]
        if obj:
            return obj
        else:
            raise IndexError

    def on_registered_changed(self, widget):
        """
        This method implements the abstract method presented on the MainWindow
        Class and uses information from MainWindow and RegisteredWindow. In
        fact, if the user chooses the personalized choice, a window appears
        with some options to define the date range of the search.
        :param widget: The ComboBoxTest Registered Choices.
        :return: None
        """
        active_id = widget.get_active_id()
        if active_id == "anytime":
            validated_data = self._validate_field(widget.get_name(),
                                                  field_type="timedelta",
                                                  status_icon=None,
                                                  hours=0,
                                                  minutes=1)
            if validated_data:
                self._register_model_value(self.registered_choices,
                                           validated_data)

        elif active_id == "personalized":
            self.regwindow.set_transient_for(self.mainwindow)
            self.regwindow.show_all()
        else:
            validated_data = self._validate_field(widget.get_name(),
                                                  field_type="timedelta",
                                                  status_icon=None,
                                                  hours=int(active_id),
                                                  minutes=0)
            if validated_data:
                self._register_model_value(self.registered_choices,
                                           validated_data)

if __name__ == "__main__":
    window = Win32LogFinderGui()
    Gtk.main()
