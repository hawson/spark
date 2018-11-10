#!/bin/bash
# random numbers beteen 1 and 20 (inclusive)
# Don't trust this for anything serious, 
# but it's probably fine for your D&D game.
while [[ 1 ]]; do
    echo $((($RANDOM % 20) + 1))
    sleep 1
done
