from .base import BaseGui, Register


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

        self.registered_choices = {}

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
        TODO:Stub for now.
        """
        raise NotImplementedError