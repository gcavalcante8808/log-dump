#!/usr/bin/env python
# -*- coding: utf-8 -*-
#__author__ = '01388863189'
#
# Done by Gabriel Abdalla Cavalcante Silva at Receita Federal do Brasil,
#
# Licensed under the Apache License, Version 2.0, that can be viewed at:
#   http://www.apache.org/licenses/LICENSE-2.0
#
"""
This module finds and dump AUDIT FAILURES on the SECURITY WINDOWS LOG into a logon_failure.log file.
"""
import win32evtlog #Just Win32EVTModule can be used for this.
import datetime #Will be usefull to define the range of the log generation.
import argparse # Will be usefull to receive some cli parameters.

"""
The class wrapps the dump_log method, that do all the job. A start time and a end time are necessary for instantiate it.
"""
class AuditFailureDump(object):
    def __init__(self, StartDate, EndDate):
        try:
            self.base_time = datetime.datetime.strptime(StartDate, "%d/%m/%y %H:%M")
            self.end_time = datetime.datetime.strptime(EndDate, "%d/%m/%y %H:%M")

        except ValueError as e:
            print ("A data informada não está no formado DIA/MES/ANO HORA:MINUTO - Ex: 01/01/01 01:01. Erro: {e}".format(e=e))
            exit()
        
        # Handle and flags needed for the search.
        self.hand = win32evtlog.OpenEventLog(None, 'Security')
        self.flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ|win32evtlog.EVENTLOG_AUDIT_FAILURE|win32evtlog.EVENTLOG_INFORMATION_TYPE
        self.num = win32evtlog.GetNumberOfEventLogRecords(self.hand)
        
    def convert_time(self, pytime):
        '''
        Convert PyTime Formated Strings into DateTimeObjects
        '''
        event_time = datetime.datetime.strptime(pytime, '%m/%d/%y %H:%M:%S')
        return event_time
    
    def read_log_entry(self):
        '''
        The entries will be generated by lazy method: yield. With this, we wont run out of RAM or CPU.
        '''
        yield win32evtlog.ReadEventLog(self.hand, self.flags, 0)

    def filter_and_write_log(self):
        with open('logon_failure.log', 'w') as file:
            while True:
                events = self.read_log_entry().next()
                
                if self.convert_time(events[0].TimeGenerated.Format()) > self.end_time: break
                
                for event in events:
                    event_time = self.convert_time(event.TimeGenerated.Format())
                    if (event.EventID == 4768 or event.EventID == 529) and ( event_time>= self.base_time):
                        file.write(str(event.EventID))
                        file.write(',')
                        file.write(str(event.StringInserts))
                        file.write('\n')
                
            win32evtlog.CloseEventLog(self.hand)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Software para Dump de Erros de Autenticacao em Logs")
    parser.add_argument('-sd', '--StartDate', required=True)
    parser.add_argument('-ed', '--EndDate', required=True)
    args = parser.parse_args()

    d = AuditFailureDump(args.StartDate, args.EndDate)
    d.filter_and_write_log()