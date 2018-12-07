#! /usr/bin
# -*- coding: UTF-8 -*-

import re

def main():

    # Read in the input
    with open('input', 'rb') as in_file:
        file_contents = in_file.readlines()

    # Sort the records
    records = map(lambda x: x.rstrip(), sorted(file_contents))

    sleep_record = {}

    # Record all the times in an easy to index way
    curr_guard = None
    fell_asleep_at = None
    for record in records:
        matches = re.findall('Guard #(\d+) begins shift', record)
        if not len(matches) == 0:
            curr_guard = matches[0]

        record_minutes = int(re.findall('\d{2}:(\d{2})', record)[0])

        if 'falls asleep' in record:
            fell_asleep_at = record_minutes

        if 'wakes up' in record:
            if not fell_asleep_at == None:
                sleep_record = log_minutes_asleep(sleep_record, curr_guard, fell_asleep_at, record_minutes)

    most_sleepy_guard = get_most_sleepy_guard(sleep_record)
    print('The most sleepy guard is #{guard_id} who slept for a total of {minutes_asleep} minutes'.format(
        guard_id=most_sleepy_guard[0],
        minutes_asleep=most_sleepy_guard[1]
    ))

    most_sleepy_minute_for_guard = get_most_sleepy_minute_for_guard(sleep_record[most_sleepy_guard[0]])
    print('The most sleepy minute for that guard was {minute} for which they were asleep a total of {minutes_asleep} minutes'.format(
        minute=most_sleepy_minute_for_guard[0],
        minutes_asleep=most_sleepy_minute_for_guard[1]
    ))

    print('The answer to the puzzle is therefore {answer}'.format(
        answer=(int(most_sleepy_guard[0]) * most_sleepy_minute_for_guard[0])
    ))

def log_minutes_asleep(records, guard_id, fell_asleep_at, woke_up_at):
    if not guard_id in records:
        records[guard_id] = {}

    records_for_guard = records[guard_id]
    print('Logging {mins} minutes asleep for guard {guard_id}'.format(
        mins=woke_up_at-fell_asleep_at,
        guard_id=guard_id
    ))
    for i in range(fell_asleep_at, woke_up_at):
        if not i in records_for_guard:
            records_for_guard[i] = 0

        records_for_guard[i] += 1

    return records

def get_most_sleepy_guard(all_records):
    most_sleepy_guard = (None, 0)
    for guard in all_records:
        minutes_asleep = reduce(lambda x, y: x + y, all_records[guard].values())
        if minutes_asleep > most_sleepy_guard[1]:
            most_sleepy_guard = (guard, minutes_asleep)

    return most_sleepy_guard

def get_most_sleepy_minute_for_guard(guard_sleep_record):
    max_sleepy_minute = (None, 0)
    for minute in guard_sleep_record:
        if guard_sleep_record[minute] > max_sleepy_minute[1]:
            max_sleepy_minute = (minute, guard_sleep_record[minute])

    return max_sleepy_minute

if __name__ == '__main__':
    main()
