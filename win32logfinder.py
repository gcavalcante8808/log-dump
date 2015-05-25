#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
# http://www.apache.org/licenses/LICENSE-2.0
#
"""
This module finds and dump AUDIT FAILURES on the SECURITY WINDOWS LOG into a
logon_failure.log file.
"""
try:
    import win32evtlog
except ImportError:
    win32evtlog = None
import datetime
import argparse
import xml.etree.cElementTree as ETree

ns = {"ms": "http://schemas.microsoft.com/win/2004/08/events/event"}


class AuditFailureDump(object):
    """
    The class wrapps the dump_log method, that do all the job. A start time and
    end time are necessary for instantiate it.
    """

    def __init__(self, **kwargs):
        """
        We receive the start date and endDate from the argparse module and we
        use it to find all logs in the especified period.
        :param StartDate: DateTimeObject - First Date of the filter
        :param EndDate: DateTimeObject - Laste Date of the Filter
        """
        self.log = kwargs.pop('log')
        order = kwargs.pop('order')

        if order == "from-end":
            order = win32evtlog.EvtQueryReverseDirection
        elif order == "from-start":
            order = win32evtlog.EvtQueryForwardDirection

        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.value = kwargs.pop('value')
        self.ids = kwargs.pop('eventids')

        ids_query = ""
        if len(self.ids) > 1:
            for eventid in self.ids:
                if eventid == self.ids[0]:
                    ids_query += "[EventID={0} ".format(eventid)
                elif eventid == self.ids[-1]:
                    ids_query += "or EventID={0}]".format(eventid)
                else:
                    ids_query += "or EventID={0}".format(eventid)
        else:
            ids_query = "[EventID={0}]".format(self.ids[0])

        
        try:
            self.base_time = datetime.datetime.strptime(self.start_date,
                                                        "%d/%m/%Y %H:%M")
            self.end_time = datetime.datetime.strptime(self.end_date,
                                                       "%d/%m/%Y %H:%M")

        except ValueError as e:
            print("""The Date Needs to Be in the format: 10/01/2015 00:00.
             Error: {e} ( %dd/%mm/%Y %H:%M)""".format(e=e))
            exit(1)

        xpath = "Event/System"
        date = self.base_time.isoformat()

        datecomp = "{0}/TimeCreated[@SystemTime > '{1}']".format(xpath, date) 
        idscomp = "{0}{1}".format(xpath, ids_query)

        self.hand = win32evtlog.EvtQuery(self.log, order, 
                                         datecomp + " and " + idscomp)

    def convert_time(self, pytime):
        """
        Convert PyTime Formated Strings into DateTimeObjects
        """
        event_time = datetime.datetime.strptime(pytime, '%m/%d/%y %H:%M:%S')
        return event_time

    def read_log_entry(self):
        """
        The entries will be generated by lazy method: yield. With this,
        we wont run out of RAM or CPU.
        """
        try:
            yield win32evtlog.EvtNext(self.hand, 1)[0]
        except (IndexError,):
            pass

    def filter_and_write_log(self):
        """
        The method will use the read_log_entry method to get the log entries,
        then it will filter for the relevant EventID's and write it into a log.
        """

        with open("logon_failure.log", "w") as logfile:
            while True:
                try:
                    entry = self.read_log_entry()
                    rendered_entry = win32evtlog.EvtRender(entry.next(), 1)
                    event = ETree.fromstring(rendered_entry)
                    s = event.find("ms:System/ms:TimeCreated",
                                   ns).get("SystemTime")

                    systime = datetime.datetime.strptime(s.rsplit(".")[0],
                                                         "%Y-%m-%dT%H:%M:%S")

                    if self.end_time > systime:
                        logfile.write(str(rendered_entry + "\n"))

                except (StopIteration, AttributeError):
                    break

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Software that dumps log
    entries from an Windows Log""")
    parser.add_argument('-l', '--log', default="Security")
    parser.add_argument('-o', '--order', choices=["from-start", "from-end"],
                        required=True)
    parser.add_argument('-sd', '--StartDate', required=True)
    parser.add_argument('-ed', '--EndDate', required=True)
    parser.add_argument('-v', '--value', required=False, default=False)
    parser.add_argument('-ids', '--eventids', nargs='+', type=int,
                        required=True)
    args = parser.parse_args()

    d = AuditFailureDump(log=args.log, order=args.order,
                         start_date=args.StartDate, end_date=args.EndDate,
                         value=args.value, eventids=args.eventids)
    d.filter_and_write_log()
