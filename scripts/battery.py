#!/usr/bin/env python3

import sys
import os
import curses
import time
import argparse


BATTERY_PATH='/sys/class/power_supply/BAT0'
SleepTime = 1

parser = argparse.ArgumentParser(description="read and report simple batter metrics, with the intention of shoving them into some graphing tool.")

parser.add_argument('--capacity', action='store_true', help="Show current %% capacity, reported by the battery")
parser.add_argument('--charge',   action='store_true', help="Show current system charge (in WHr?)")
parser.add_argument('--current',  action='store_true', help="Show current draw.")
parser.add_argument('--voltage',  action='store_true', help="Show current voltage.")
parser.add_argument('--sleep',    action='store', type=float,  help="Show current voltage.")
parser.add_argument('--path',     type=str)

try:
    parsed_arguments = parser.parse_args()
except SystemExit as e:
    print("Bad arguments, or something")
    sys.exit(1)


parsed_args = vars(parsed_arguments)

if parsed_args['path']:
    BATTERY_PATH = parsed_args['path']

if parsed_args['sleep']:
    SleepTime = parsed_args['sleep']


del parsed_args['path']
del parsed_args['sleep']

files = {
    'capacity': 'capacity',
    'charge':   'charge_now',
    'current':  'current_now',
    'voltage':  'voltage_now',
}


fds = {}

active_files = list(map( lambda y: files[y], filter( lambda x: parsed_args[x] is True, parsed_args.keys())))
for fname in active_files:
    try:
        filename = BATTERY_PATH+'/'+fname
        fd = open(filename,'r')

    except OSError as err:
        print("Error opening [{}]: {}".format(filename, err.strerror))
        sys.exit(1)

    fds[fname]=fd

try:
    while True:
        output = {}
        for fname in active_files:
            fds[fname].seek(0,0)
            output[fname] = fds[fname].readline().strip()

        for fname in active_files:
            print("%s" % output[fname], end=' ')

        print('')
        sys.stdout.flush()
        
        time.sleep(SleepTime)

except KeyboardInterrupt:
    for fd in fds:
        fds[fd].close()

sys.exit(0)
