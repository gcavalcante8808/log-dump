import weakref
from .base import BaseGui


class Register(object):
    """
    An class that functions as a Interface, containing basic data about the
    RegisterWindow Fields.
    """

    def __init__(self, name):
        """
        All instances should be tracked using the name.
        """
        self.__class__.instances.append(weakref.proxy(self))
        self.name = name

    model = None
    choices = None
    field_date = None
    field_time = None
    field_date_status = None
    field_time_status = None

    instances = []

    @property
    def fields(self):
        """
        Return the two fields as one.
        """
        return self.field_date, self.field_time

    @property
    def fields_statuses(self):
        """
        Return the two field status attrs as one
        """
        return self.field_date_status, self.field_time_status


class RegisteredWindow(BaseGui):
    """
    Contain all information about the DateRange Dialog - Registered Window.
    """

    def __init__(self):
        """
        Get the RegisteredWindow from the glade file, instantiate and map
        Register Class instances  and their fields to the glade Gtk widgets.
        """
        super(RegisteredWindow, self).__init__()
        self.regwindow = self.builder.get_object("RegisteredWindow")

        self.from_field = Register(name="from_field")
        self.from_field.model = self.registered_choices
        self.from_field.choices = self.builder.get_object("from_field_choices")
        self.from_field.field_date = self.builder.get_object("from_field_date")
        self.from_field.field_time = self.builder.get_object("from_field_time")
        self.from_field.field_date_status = \
            self.builder.get_object("from_date_status")
        self.from_field.field_time_status = \
            self.builder.get_object("from_time_status")

        self.to_field = Register(name="to_field")
        self.to_field.model = self.registered_choices
        self.to_field.choices = self.builder.get_object("to_field_choices")
        self.to_field.field_date = self.builder.get_object("to_field_date")
        self.to_field.field_time = self.builder.get_object("to_field_time")
        self.to_field.field_date_status = \
            self.builder.get_object("to_date_status")
        self.to_field.field_time_status = \
            self.builder.get_object("to_time_status")

    def on_register_choice_changed(self, widget):
        """
        Receive the widget values and write/disable/enables some fields on GtkUI

        If the user chooses first event or last event, automatic values are
        writen on instance.model.
        """
        widget_value = widget.get_active_id()
        instance = self._object_picker(widget.get_name())[0]

        values = {instance.field_date.get_name(): "event",
                  instance.field_time.get_name(): "date"}

        if "event" in widget_value:
            if values:
                self._register_model_value(instance.model, values)
                self._toggle_fields(instance.fields, operation="disable")

        elif "date" in widget_value:
            self._toggle_fields(instance.fields, operation="enable")

    def on_field_date_changed(self, widget):
        """
        Receive Widgets values that comes from date fields on GtkUI and register
        the value if it is valid.
        """
        value = widget.get_text()
        instance = self._object_picker(widget.get_name())[0]
        validated_data = self._validate_field(
            field=instance.field_date.get_name(), field_type="date",
            value=value, status_icon=instance.field_date_status)

        if validated_data:
            self._register_model_value(instance.model, validated_data)

    def on_field_time_changed(self, widget):
        """
        Receive Widgets values that comes from time fields on GtkUI and register
        the value if it is valid.
        """
        value = widget.get_text()
        instance = self._object_picker(widget.get_name())[0]
        validated_data = self._validate_field(
            field=instance.field_time.get_name(), field_type="time",
            value=value, status_icon=instance.field_time_status)

        if validated_data:
            self._register_model_value(instance.model, validated_data)

    def on_rwindow_ok_button_clicked(self, widget):
        """
        Stub for now.
        """
        print(self.registered_choices)