#!/bin/sh
if [[ -z "$1" ]]; then
    echo "Enter a hostname or IP to ping."
    exit 1
fi
I=${2:-1}
ping -n -i $I $1 | awk '/^[0-9]/{print gensub("time=","",1,$7); fflush()}'
