#!/usr/bin/env python3
import sys

current_location = None
total_duration = 0
count = 0
header_printed = False

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        location, duration = line.split("\t")
        duration = float(duration)
    except:
        continue

    if current_location is None:
        current_location = location

    if location == current_location:
        total_duration += duration
        count += 1
    else:
        if not header_printed:
            print("Location\tCount\tAverage_Duration")
            header_printed = True

        avg = total_duration / count if count else 0
        print(f"{current_location}\t{count}\t{avg:.2f}")
        current_location = location
        total_duration = duration
        count = 1

# Print last group
if current_location:
    if not header_printed:
        print("Location\tCount\tAverage_Duration")
    avg = total_duration / count if count else 0
    print(f"{current_location}\t{count}\t{avg:.2f}")