#!/usr/bin/bash

pid=$(ps aux | grep controlRobot | grep -v grep | awk '{print $2}')

if [ -z "$pid" ]; then
    echo "--------"
    echo $(date)
    echo "Starting Control Robot"
    cd /home/caninos/projeto
    screen -dmS controlRobot -L -Logfile /home/caninos/logs/robcontrol.log python3 -m robcontrol -s --log-level INFO
fi
