#!/bin/bash

INDEX=${1:-0}
while [[ 1 ]]; do
    read -a LOAD < /proc/loadavg
    echo ${LOAD[$INDEX]}
    sleep 2.5
done
