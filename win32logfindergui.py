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
import datetime
import weakref


class BaseGui(object):
    """
    A simple Base Class that will contain information needed by all other classes.
    """
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.registered_choices = {}

    def _register_model_value(self, model, value):
        """
        Receive a value and inserts into the especified dictionary.
        :param field:
        :param value:
        :return:
        """
        model.update(value)

    def _toggle_fields(self, fields, operation):
        if operation == "disable":
            for field in fields:
                field.set_property("editable", False)
        elif operation == "enable":
            for field in fields:
                field.set_property("editable", True)

    def _object_picker(self, widget_name):
        obj = [obj for obj in Register.instances if obj.name in widget_name]
        if obj:
            return obj
        else:
            raise IndexError

    def _validate_field(self, field, field_type, value, status_icon):
        """
        Validate a field accordingly to the field type, as follows:

        Text: if the field is not null, it is validated.
        Date: If the string can be converted to datetime, it is validated.
        Time: If the string can be converted to hour/minute, it is validated.

        In all cases, if the field is valid, the correspondent icon of status is updated.
        """
        validated_data = None

        if field_type == "text":
            pass
        #TODO: STOCK_DIALOG_WARNING_WONT_WORK
        elif field_type == "date":
            try:
                validated_data = datetime.datetime.strptime(value, "%d/%m/%Y")
            except (ValueError,):
                if status_icon.get_stock()[0] != "gtk-dialog-warning":
                    status_icon.set_from_icon_name(Gtk.STOCK_DIALOG_WARNING, 4)

        elif field_type == "time":
            try:
                validated_data = datetime.datetime.strptime(value, "%H:%M")
            except(ValueError,):
                if status_icon.get_stock()[0] != "gtk-dialog-warning":
                    status_icon.set_from_icon_name(Gtk.STOCK_CLOSE, 4)

        if validated_data:
            status_icon.set_from_icon_name(Gtk.STOCK_APPLY, 4)
            return {field: validated_data}


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
        self.mainwindow = self.builder.get_object("MainWindow")

    @abc.abstractmethod
    def on_registered_changed(self, widget):
        """
        This method has some relationship with the RegisteredWindow Class, and will be implemented on the GUI itself,
        not here.
        """
        pass

    def on_delete_window(self, widget):
        Gtk.main_quit()

    def on_search_clicked(self, widget):
        raise NotImplementedError

    def on_clear_clicked(self, widget):
        raise NotImplementedError

    def on_about_activated(self, widget):
        raise NotImplementedError

    def on_search_order_cb_changed(self, widget):
        raise NotImplementedError


class Register(object):
    def __init__(self, name=None):
        self.__class__.instances.append(weakref.proxy(self))
        self.name = name

    model = None
    choices = None
    field_date = None
    field_time = None
    field_date_status = None
    field_time_status =None

    instances = []

    @property
    def fields(self):
        return self.field_date, self.field_time

    @property
    def fields_statuses(self):
        return self.field_date_status, self.field_time_status


class RegisteredWindow(BaseGui):
    def __init__(self):
        super(RegisteredWindow, self).__init__()
        self.regwindow = self.builder.get_object("RegisteredWindow")

        self.from_field = Register(name="from_field")
        self.from_field.model = self.registered_choices
        self.from_field.choices = self.builder.get_object("from_field_choices")
        self.from_field.field_date = self.builder.get_object("from_field_date")
        self.from_field.field_time = self.builder.get_object("from_field_time")
        self.from_field.field_date_status = self.builder.get_object("from_date_status")
        self.from_field.field_time_status = self.builder.get_object("from_time_status")

        self.to_field = Register(name="to_field")
        self.to_field.model = self.registered_choices
        self.to_field.choices = self.builder.get_object("to_field_choices")
        self.to_field.field_date = self.builder.get_object("to_field_date")
        self.to_field.field_time = self.builder.get_object("to_field_time")
        self.to_field.field_date_status = self.builder.get_object("to_date_status")
        self.to_field.field_time_status = self.builder.get_object("to_time_status")

    def on_register_choice_changed(self, widget):
        widget_value = widget.get_active_id()
        instance = self._object_picker(widget.get_name())[0]

        values = {instance.field_date.get_name(): "event", instance.field_time.get_name(): "date"}

        if "event" in widget_value:
            if values:
                self._register_model_value(instance.model, values)
                self._toggle_fields(instance.fields, operation="disable")

        elif "date" in widget_value:
            self._toggle_fields(instance.fields, operation="enable")

    def on_field_date_changed(self, widget):
        value = widget.get_text()
        instance = self._object_picker(widget.get_name())[0]
        validated_data = self._validate_field(field=instance.field_date.get_name(), field_type="date", value=value,
                                              status_icon=instance.field_date_status)

        if validated_data:
            self._register_model_value(instance.model, validated_data)

    def on_field_time_changed(self, widget):
        value = widget.get_text()
        instance = self._object_picker(widget.get_name())[0]
        validated_data = self._validate_field(field=instance.field_time.get_name(), field_type="time", value=value,
                                              status_icon=instance.field_time_status)

        if validated_data:
            self._register_model_value(instance.model, validated_data)

    def on_rwindow_ok_button_clicked(self, widget):
        print(self.registered_choices)


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
