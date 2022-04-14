#!/usr/bin/env python

import os, sys, csv
import os.path

#get this file's path (should be $SPLUNK_HOME/etc/apps/app_name/bin)
this_file_path = os.path.split(os.path.abspath(__file__))
path_info = this_file_path[0].split('/')

# create the filepath for the lookups (up one, then to lookups folder)
csv_path_end = "lookups/rangemap.csv"
csv_path=""
for i in range (1,len(path_info)-1):
    csv_path=csv_path+"/"+path_info[i]
csv_path=csv_path+"/"+csv_path_end

# create the filepath for the tags.conf (up one, then to local folder)
write_file_end = "local/tags.conf"
write_file_path = ""
for i in range (1,len(path_info)-1):
    write_file_path=write_file_path+"/"+path_info[i]
write_file_path=write_file_path+"/"+write_file_end

# remove the current tags.conf - probably isn't totally necessary if I open the file with a "w"
os.remove(write_file_path)

# open a new tags.conf
conf_file = open(write_file_path,"w")

# read the csv
with open (csv_path) as csv_file:
    info_file = csv.reader(csv_file, delimiter=',')
    # read each row and write the description to the tags.conf
    for row in info_file:
        # skip the first row
        if (row[1].strip()=='description'):
            continue
        """writes the following two lines into tags.conf:
        [eventtype=<description>]
        <description> = enabled"""
        conf_file.write('[eventtype='+row[1].strip()+']\n')
        conf_file.write(row[1].strip()+' = enabled\n\n')

# close the new tags.conf
conf_file.close()

"""Things you may want to also do:
1. Generate a token and hit the debug/refresh endpoint at the end of this script

2. Cron schedule this script to run sometime after the saved search generating an updated lookup

3. Update this script to python 3.7 before doing anything that messes with Splunk endpoints or other more complicated extensions of the script above
"""
