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
            print ("A data informada não está no formado DIA/MES/ANO HORA:MINUTO - Ex: 01/01/01 01:01")
            exit()
            
    def dump_log(self):
            # Handle and flags needed for the search.
        hand = win32evtlog.OpenEventLog(None, 'Security')
        flags = win32evtlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ|win32evtlog.EVENTLOG_AUDIT_FAILURE|win32evtlog.EVENTLOG_INFORMATION_TYPE
        num = win32evtlog.GetNumberOfEventLogRecords(hand)

        # Fields returned for the Win2k8 Eventlog Entries
        FIELDS_2K8 = 'time, account,realm,userid,service,service_id,client_address,client_port, ticket_ops,\
        ticket_result_code, ticket_enctypes, preauth_type, cert_issuer, cert_serial, cert_thumb'

        with open('logon_failure.log', 'w') as file:
            file.write(str(FIELDS_2K8))
            file.write('\n')
            # We need to iterate over various loops because the eventlog lib dont return more than 10 results. 
            # We will iter until all results are loaded.
            for i in xrange(num):
                events = win32evtlog.ReadEventLog(hand, flags, 0)
                #if we dont have more events to iter over, break.
                if not events: break
                i = i+len(events)
                # Time provided by the user.
                # base_time = (datetime.datetime(2013,11,25,16,00))
                for event in events:
                    # We need to convert the TimeGenerated 'Pyttime' type into Datetime to use the compare using timedelta nearly there.
                    event_time = datetime.datetime.strptime(event.TimeGenerated.Format(), '%m/%d/%y %H:%M:%S')
                    if event.EventID == 4768 and (event_time >= self.base_time) and (event_time < self.end_time):
                    # write the result into the log file.
                        file.write(event.TimeGenerated.Format())
                        file.write(',')
                        file.write(str(event.StringInserts))
                        file.write('\n')
        # Close the handler.
        win32evtlog.CloseEventLog(hand)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Software para Dump de Erros de Autenticacao em Logs")
    parser.add_argument('-sd', '--StartDate', required=True)
    parser.add_argument('-ed', '--EndDate', required=True)
    args = parser.parse_args()
    
    d = AuditFailureDump(args.StartDate, args.EndDate)
    d.dump_log()