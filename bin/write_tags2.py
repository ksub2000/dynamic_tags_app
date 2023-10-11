#!/usr/bin/env python3

import os
import csv

# Get this file's path (should be $SPLUNK_HOME/etc/apps/app_name/bin)
this_file_path = os.path.abspath(__file__)
path_info = os.path.dirname(this_file_path).split(os.sep)

# Create the filepath for the lookups (up one, then to lookups folder)
csv_path_end = "lookups/rangemap.csv"
csv_path = os.path.join(*path_info[:-1], csv_path_end)

# Create the filepath for the tags.conf (up one, then to local folder)
write_file_end = "local/tags.conf"
write_file_path = os.path.join(*path_info[:-1], write_file_end)

# Remove the current tags.conf - probably isn't totally necessary if opening the file with "w"
if os.path.exists(write_file_path):
    os.remove(write_file_path)

# Open a new tags.conf
with open(write_file_path, "w") as conf_file:
    # Read the CSV
    with open(csv_path, newline='') as csv_file:
        info_file = csv.reader(csv_file, delimiter=',')
        # Read each row and write the description to the tags.conf
        for row in info_file:
            # Skip the first row
            if row[1].strip() == 'description':
                continue
            # Write the following two lines into tags.conf:
            # [eventtype=<description>]
            # <description> = enabled
            conf_file.write(f'[eventtype={row[1].strip()}]\n')
            conf_file.write(f'{row[1].strip()} = enabled\n\n')

"""Things you may want to also do:
1. Generate a token and hit the debug/refresh endpoint at the end of this script

2. Cron schedule this script to run sometime after the saved search generating an updated lookup

3. [DONE] Update this script to python 3.7 before doing anything that messes with Splunk endpoints or other more complicated extensions of the script above
"""