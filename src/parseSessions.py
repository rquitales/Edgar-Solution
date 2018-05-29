# -*- coding: utf-8 -*-
import csv, datetime, sys
from collections import OrderedDict

#Parse bash variables (input files and output file to write to).
logfile = sys.argv[1]
interval = datetime.timedelta(seconds = int(open(sys.argv[2], 'r').read()))
filewriter = open(sys.argv[3], 'w')

#Define sessionization.txt output file writing function.
def writeEntry(ipAddress):
    filewriter.write(ipAddress + "," + log[ipAddress][0].strftime("%Y-%m-%d %H:%M:%S") + "," +  log[ipAddress][1].strftime("%Y-%m-%d %H:%M:%S") + "," +  str(log[ipAddress][2]) + "," +  str(log[ipAddress][3]) + '\n')

#Initialize empty OrderedDict for logging of sessions.
log = OrderedDict()

#Open log.csv and sequentially process each line.
with open(logfile, 'r') as csvfile:
    for row in csv.DictReader(csvfile):
        #Extract ip and date/time fields from log.csv.
        ip = row['ip']
        time = datetime.datetime.strptime("{}, {}".format(row['date'], row['time']), "%Y-%m-%d, %H:%M:%S")

        #Check if any sessions are inactive in ordered dict. Write/log it and remove from ordered dict.
        expired = [j for j in log if time - log[j][1] > interval]
        if len(expired) > 0:
            for ipAddress in expired:
                writeEntry(ipAddress)
                del log[ipAddress]

        #Check if ip address of current line is in ordered dict. If present, modify its entry and continue to next line.
        if ip in log:
            log[ip][1] = time
            log[ip][2] = int((time - log[ip][0]).total_seconds() + 1)
            log[ip][3] += 1
            continue

        #Add new entry to ordered dict.
        log[ip] = [time, time, 1, 1]

    #Once csv iteration ends, write contents of ordered dictionary to sessionization.txt as all sessions now ended.
    for ipAddress in log:
        writeEntry(ipAddress)
filewriter.close()
