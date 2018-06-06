#!/usr/bin/env python3

import argparse

import datetime

TZ_DICT = {'CET': 1,
           'CEST': 2,
           'PST': -8,
           'PDT': -7,
           'JST': 9,
           'MSD': 4,
           'MSK': 3,
           'AET': 10,
           'AEDT': 11,
           'HST': -10,
           'HDT': -9,
           'MST': -7,
           'MDT': -6}

def get_timestring(some_datetime):
    if some_datetime.hour < 10:
        hourdiff = '0%s' % some_datetime.hour
    else:
        hourdiff = some_datetime.hour

    if some_datetime.minute < 10:
        mindiff = '0%s' % some_datetime.minute
    else:
        mindiff = some_datetime.minute

    time = '%s%s' % (hourdiff, mindiff)
    return time

def convert_time(atime, difference, tz):

    timediff = atime + datetime.timedelta(hours=difference)

    time = get_timestring(timediff)
    original = get_timestring(atime)

    message = ('%s evetime is %s %s ' % (
    original, time, tz))

    return message

def main(args):
    if len(args.time) < 4:
        return 'time should be a 4 digit number, ie. 0815, 1530'

    hours = args.time[:2]
    minutes = args.time[2:]

    evetime = datetime.datetime(
        year=1990,
        month=4,
        day = 14,
        hour=int(hours),
        minute=int(minutes)
    )

    message = []
    for timezone in args.timezone:
        if timezone.upper() not in TZ_DICT.keys():
            return 'please use one of %s' % ', '.join(TZ_DICT)
        else:
            difference = int(TZ_DICT.get(timezone.upper()))

        message.append(convert_time(evetime, difference, timezone))
    return '\n'.join(message)


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='find timezones around eve time')
    PARSER.add_argument('time', help='the time to convert, in the format HHMM '
                                     'as military time i.e. 0830, 1545')
    PARSER.add_argument('timezone', help='timezone abbreviations, one of: \n%s'
                                         % ', '.join(TZ_DICT.keys()),
                        nargs='*')
    ARGS = PARSER.parse_args()
    print(main(ARGS))