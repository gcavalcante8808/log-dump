import datetime
import weakref
from gi.repository import Gtk


class BaseGui(object):
    """
    A simple Base Class that will contain information needed by all other
    classes.
    """

    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui.glade")
        self.registered_choices = {}

    @staticmethod
    def _object_picker(widget_name):
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

    @staticmethod
    def _register_model_value(model, value):
        """
        Receive a value and inserts into the especified dictionary/model.
        :param model: The name of the data model, eg registered choices.
        :param value: Dictionary to be inserted into the model.
        :return: None
        """
        model.update(value)

    @staticmethod
    def _toggle_fields(fields, operation):
        """
        Activates and deactivates some Gtk Fields.
        :param fields: List of Gtk fields.
        :param operation: Enable or Disable.
        :return: None
        """
        if operation == "disable":
            for field in fields:
                field.set_property("editable", False)
        elif operation == "enable":
            for field in fields:
                field.set_property("editable", True)

    @staticmethod
    def _validate_field(field, field_type, status_icon=None, regexp=None,
                        **kwargs):
        """
        Validate a field accordingly to the field type, as follows:

        Text: if the field is not null, it is validated.
        Date: If the string can be converted to datetime, it is validated.
        Time: If the string can be converted to hour/minute, it is validated.
        Regexp: If the string matches for the needed regexp, it is validated.
        DeltaTime: If the value provided can match the Difference between
        some hours in DeltaTimeObject python, it is validated.

        In all cases, if the field is valid, the correspondent icon of status
        is updated.
        """
        validated_data = None

        if field_type == "text":
            value = kwargs.pop("value")
            if value:
                validated_data = value

        elif field_type == "regexp":
            if regexp.match(kwargs.pop("value")):
                validated_data = True
        # TODO: STOCK_DIALOG_WARNING_WONT_WORK
        # TODO: DATE AND TIME TYPES SHOULD BE MERGED.
        elif field_type == "date":
            try:
                validated_data = datetime.datetime.strptime(kwargs.pop("value"),
                                                            "%d/%m/%Y")
            except (ValueError,):
                pass

        elif field_type == "time":
            try:
                time = datetime.datetime.strptime(kwargs.pop("value"), "%H:%M")
                validated_data = datetime.timedelta(hours=time.hour,
                                                    minutes=time.minute)
            except(ValueError,):
                pass

        elif field_type == "timedelta":
            try:
                now = datetime.datetime.now()
                diff = datetime.timedelta(hours=kwargs.pop('hours'),
                                          minutes=kwargs.pop('minutes'))
                validated_data = now - diff
                return {"to_field": validated_data, "from_field": now}

            except(ValueError,):
                pass

        if validated_data:
            if status_icon:
                status_icon.set_from_icon_name(Gtk.STOCK_APPLY, 4)
            return {field: validated_data}

        else:
            if status_icon and status_icon.get_stock()[0] != \
                    "gtk-dialog-warning":
                status_icon.set_from_icon_name(Gtk.STOCK_CLOSE, 4)


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
