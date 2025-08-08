#!/usr/bin/env python3
import sys
import csv

reader = csv.reader(sys.stdin)
for row in reader:
    try:
        location = row[0].strip()
        duration = float(row[1].strip())
        print(f"{location}\t{duration}")
    except:
        continue