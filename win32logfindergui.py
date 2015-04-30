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


class Win32LogFinderGui(Gtk.Window):

    def get_all_values(self, widget):
        order = self.order_choices.get_active_text()
        flags = self.flag_choices.get_active_text()
        start_date = self.sdate_content.get_date()
        end_date = self.edate_content.get_date()
        print(order, flags, start_date, end_date)

    def on_combobox_change(self, widget):
        print(widget.get_active_text(), widget.get_title())

    def on_calendar_change(self, widget):
        print(widget.get_date(), widget.get_composite_name())

    def __init__(self):
        Gtk.Window.__init__(self, title="Win32LogFinder")

        info = Gtk.Label("""Please fill the entries bellow to search and filter
                         entries in the Windows Eventlog.""")

        info.set_justify(Gtk.Justification.CENTER)

        self.log_label = Gtk.Label("Event Log")
        self.log_content = Gtk.Entry()
        self.log_content.set_text("Event Log Name")

        self.order_label = Gtk.Label("Search Order")
        self.order_choices = Gtk.ComboBoxText()
        self.order_choices.set_title("Order")
        self.order_choices.insert(0, "0", "From the Newest to Oldest")
        self.order_choices.insert(1, "1", "From the Oldest to Newest")

        self.flag_label = Gtk.Label("Event Type")
        self.flag_choices = Gtk.ComboBoxText()
        self.flag_choices.set_title("Flag")
        self.flag_choices.insert(0, "0", "EVENTLOG_ERROR_TYPE")
        self.flag_choices.insert(1, "1", "EVENTLOG_WARNING_TYPE")
        self.flag_choices.insert(2, "2", "EVENTLOG_INFORMATION_TYPE")
        self.flag_choices.insert(3, "3", "EVENTLOG_AUDIT_SUCCESS")
        self.flag_choices.insert(4, "4", "EVENTLOG_AUDIT_FAILURE")

        self.sdate_label = Gtk.Label("Start Period")
        self.sdate_content = Gtk.Calendar()
        self.sdate_content.set_composite_name = "StartDate"

        self.edate_label = Gtk.Label("End Period")
        self.edate_content = Gtk.Calendar()
        self.edate_content.set_composite_name = "EndDate"

        self.action_button = Gtk.Button(label="Start Search")
        self.action_button.connect("clicked", self.get_all_values)

        grid = Gtk.Grid(row_spacing=25, column_spacing=20)
        self.add(grid)

        grid.add(info)
        grid.attach(self.log_label, 0, 1, 1, 1)
        grid.attach_next_to(self.log_content, self.log_label, RIGHT, 1, 1)

        grid.attach_next_to(self.order_label, self.log_label, BOTTOM, 1, 1)
        grid.attach_next_to(self.order_choices, self.order_label, RIGHT, 1, 1)

        grid.attach_next_to(self.flag_label, self.order_label, BOTTOM, 1, 1)
        grid.attach_next_to(self.flag_choices, self.flag_label, RIGHT, 1, 1)

        grid.attach_next_to(self.sdate_label, self.flag_label, BOTTOM, 1, 1)
        grid.attach_next_to(self.sdate_content, self.sdate_label, RIGHT, 1, 1)

        grid.attach_next_to(self.edate_label, self.sdate_label, BOTTOM, 1, 1)
        grid.attach_next_to(self.edate_content, self.edate_label, RIGHT, 1, 1)

        grid.attach_next_to(self.action_button, self.edate_label, BOTTOM, 2, 1)

win = Win32LogFinderGui()
win.connect("delete-event", Gtk.main_quit)
win.show_all()
Gtk.main()