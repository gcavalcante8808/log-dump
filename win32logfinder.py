#!/usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva at Receita Federal do Brasil,
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
        self.order = kwargs.pop('order')
        self.flag = kwargs.pop('flags')
        self.start_date = kwargs.pop('start_date')
        self.end_date = kwargs.pop('end_date')
        self.value = kwargs.pop('value')
        self.ids = kwargs.pop('eventids')

        try:
            self.base_time = datetime.datetime.strptime(self.start_date,
                                                        "%d/%m/%y %H:%M")
            self.end_time = datetime.datetime.strptime(self.end_date,
                                                       "%d/%m/%y %H:%M")

        except ValueError as e:
            print """The Date Needs to Be in the format: 10/01/15 00:00.
             Error: {e}""".format(e=e)
            exit(1)

        # Handle and flags needed for the search.
        self.hand = win32evtlog.OpenEventLog(None, self.log)
        seq = win32evtlog.EVENTLOG_SEQUENTIAL_READ
        self.flags = self.order | seq | self.flag
        self.num = win32evtlog.GetNumberOfEventLogRecords(self.hand)

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
        yield win32evtlog.ReadEventLog(self.hand, self.flags, 0)

    def filter_and_write_log(self):
        """
        The method will use the read_log_entry method to get the log entries,
        then it will filter for the relevant EventID's and write it into a log.
        """
        with open('logon_failure.log', 'w') as logon_file:
            logon_file.write("""EventID, SID, Principal, Ticket Options,
            Error ID, Preauth Type, IP\n""")
            while True:
                events = self.read_log_entry().next()
                if events:
                    if self.convert_time(events[0].TimeGenerated.Format()) > \
                            self.end_time:
                        break

                    for event in events:
                        etime = self.convert_time(event.TimeGenerated.Format())

                        if event.EventID in self.ids and \
                                (etime >= self.base_time):
                            logon_file.write(str(event.EventID))
                            logon_file.write(',')
                            logon_file.write(str(event.StringInserts))
                            logon_file.write('\n')
                else:
                    break

            win32evtlog.CloseEventLog(self.hand)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="""Software that dumps log
    entries from an Windows Log""")
    parser.add_argument('-l', '--log', default="Security")
    parser.add_argument('-o', '--order', choices=["from-start", "from-end"])
    parser.add_argument('-f', '--flags', choices=["ERROR", "WARNING",
                                                  "INFORMATION", "SUCCESS",
                                                  "FAILURE"])
    parser.add_argument('-sd', '--StartDate', required=True)
    parser.add_argument('-ed', '--EndDate', required=True)
    parser.add_argument('-v', '--value', required=False, default=False)
    parser.add_argument('-ids', '--eventids', nargs='+', type=int,
                        required=True)
    args = parser.parse_args()

    flag = None
    if args.flags == "ERROR":
        flag = win32evtlog.EVENTLOG_ERROR_TYPE
    elif args.flags == "WARNING":
        flag = win32evtlog.EVENTLOG_WARNING_TYPE
    elif args.flags == "INFORMATION":
        flag = win32evtlog.EVENTLOG_INFORMATION_TYPE
    elif args.flags == "SUCCESS":
        flag = win32evtlog.EVENTLOG_AUDIT_SUCCESS
    elif args.flags == "FAILURE":
        flag = win32evtlog.EVENTLOG_AUDIT_FAILURE

    order = None
    if args.order == "from-end":
        order = win32evtlog.EVENTLOG_BACKWARDS_READ
    elif args.order == "from-start":
        order = win32evtlog.EVENTLOG_FORWARDS_READ

    d = AuditFailureDump(log=args.log, order=order, flags=flag,
                         start_date=args.StartDate, end_date=args.EndDate,
                         value=args.value, eventids=args.eventids)
    d.filter_and_write_log()
