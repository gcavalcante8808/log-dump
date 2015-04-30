log-dump
--------

The Windows security log dumper.

Introduction
------------

Log-Dump is a Python script to dump and filter Windows Logon Events of all kind on Windows 2008 / 2012 Servers and on Windows 2003 Servers.
With this tool, system admins can generate a CSV list with all information contained in the Windows Log, which became easily to treat.

Installation
------------

1. Install Log-dump.

You can install the log-dump through pip:

`pip install log-dump`

As well, the sdist package can be downloaded at:

https://pypi.python.org/pypi/log-dump/

Compiled Version (No Installation or python environment setup needed)

If you just want to use the utility, you can download it directly from:

http://ts3corp.com.br/dnl/

We recommend a md5aum verify before any use. The md5sum file is provided in the same url.

How to Use
----------

Once Installed, you just need run it with Elevated Privileges and provide the following information:

log - The Name of The Windows Log. You can see the name in the eventviewer software if you're not certain about the name.

order - The order where the log will be scaned. Options:
 * from-start: oldest to newest.
 * from-end: newest to oldest.

flags - The type of the event which will be finded. Options:
 * ERROR: Valid for all logs except audit logs, indicates EVENTLOG_ERROR_TYPE.
 * INFORMATION: Valid for all logs except audit logs, indicates EVENTLOG_INFORMATION_TYPE.
 * SUCCESS: Valid for all logs expect audit logs, indicates EVENTLOG_SUCCESS_TYPE.
 * FAILURE: Valid for audit logs, indicates EVENTLOG_AUDIT_FAILURE.
 * SUCCESS: Valid for audit logs, indicates EVENTLOG_AUDIT_SUCCESS.

StartDate - The start period in the following format: "30/01/13 20:00"

EndDate - The end period in the following format:"31/01/13 20:00"

Two examples are presented bellow (assumes that you have the python on your path):

Short Version
`C:\>log_dump.py -l Security -o from-start -f FAILURE -sd "30/01/13 20:00" -ed "31/01/13 20:00" -ids 4769`

Long Version
`C:\>log_dump.py --log Security --order from-start --flags FAILURE -StartDate "30/01/13 20:00" -EndDate "31/01/13 20:00" --eventids 4769`


A file named 'logon_failure.log' will be created at the current dir with all logon errors in the CSV format.

License
-------

Licensed under the Apache License, Version 2.0, that can be viewed at:
  http://www.apache.org/licenses/LICENSE-2.0

Credits
-------
* [Gabriel Abdalla Cavalcante](https://github.com/gcavalcante8808)
