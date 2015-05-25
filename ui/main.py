from .base import BaseGui
from gi.repository import Gtk
import abc
import re


class MainWindow(BaseGui):
    """
    The class that holds the main methods for the Main Window of the project,
    which is used by the Win32LogFinderGui class.
    """

    def __init__(self):
        """
        Just Get the Main Window object from the glade file.
        """
        super(MainWindow, self).__init__()
        self.mainwindow = self.builder.get_object("MainWindow")

        self.server_status = self.builder.get_object("server_status")
        self.eventids_status = self.builder.get_object("eventids_status")

        self.servers = {}
        self.log = {}
        self.eventids ={}

        self.order = {}

    @abc.abstractmethod
    def on_registered_changed(self, widget):
        """
        This method has some relationship with the RegisteredWindow Class, and
        will be implemented on the GUI itself, not here.
        """
        pass

    @staticmethod
    def on_delete_window(widget):
        Gtk.main_quit()

    def on_server_content_changed(self, widget):
        ipv4_regexp = r"(?:[0-9]{1,3}\.){3}[0-9]{1,3}"
        domain_regexp = r"[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,6}"
        regexp = ipv4_regexp + "|" + domain_regexp
        regexp = re.compile(regexp)
        values = widget.get_text().rsplit(",")
        for value in values:
            self._validate_field(value=value, field_type="regexp",
                                 regexp=regexp, status_icon=self.server_status,
                                 field=widget.get_name())

        if self.server_status.get_stock() is not ('gtk-dialog-warning', 4):
            self._register_model_value(self.servers, {"servers": values})

    def on_eventlog_content_activate(self, widget):
        value = widget.get_text()
        regexp = re.compile(r'[A-Za-z\-]')
        validated_data = self._validate_field(field=widget.get_name(),
                                              field_type="regexp",
                                              regexp=regexp,
                                              value=value)

        if validated_data:
            self._register_model_value(self.log, validated_data)

    @abc.abstractmethod
    def on_search_clicked(self, widget):
        raise NotImplementedError

    # @abc.abstractstaticmethod
    def on_clear_clicked(self, widget):
        raise NotImplementedError

    def on_about_activated(self, widget):
        raise NotImplementedError

    def on_eventid_content_changed(self, widget):
        values = widget.get_text().rsplit(",")
        regexp = re.compile(r"\d+")
        validated_data = None

        for value in values:
            validated_data = self._validate_field(field=widget.get_name(),
                                                  field_type="regexp",
                                                  regexp=regexp, status_icon=
                                                  self.eventids_status,
                                                  value=value)

        if self.server_status.get_stock() is not ('gtk-dialog-warning', 4):
                self._register_model_value(self.eventids,
                                           {widget.get_name(): values})

    def on_search_order_cb_changed(self, widget):
        value = widget.get_active_id()
        regexp = re.compile(r'[A-Za-z\-]')
        validated_data = self._validate_field(field=widget.get_name(),
                                              field_type="regexp",
                                              regexp=regexp,
                                              value=value)

        if validated_data:

            self._register_model_value(self.order, {"order": value})
