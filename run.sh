#!/bin/bash

if command -v python3 &>/dev/null; then
    python3 ./src/parseSessions.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
else
    python ./src/parseSessions.py ./input/log.csv ./input/inactivity_period.txt ./output/sessionization.txt
fi

