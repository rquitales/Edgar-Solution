#!/bin/bash
#
# Use this shell script to compile (if necessary) your code and then execute it. Below is an example of what might be found in this file if your program was written in Python
#
if command -v python3 &>/dev/null; then
    python3 ./src/parseSessions.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
else
    python ./src/parseSessions.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
fi

