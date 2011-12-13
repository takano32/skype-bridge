#!/bin/bash

export XAUTHORITY=/home/takano32/.Xauthority
export DISPLAY=:16

PID=0

while :;
do
  ps -p $PID > /dev/null 2>&1
  EXISTS=$?
  if [ $EXISTS -ne 0 ]; then
    echo 'doesnt exist process and bootup'
    LANG=C date
    sudo -u gree -E /usr/bin/skype &
    PID=$!
    trap "kill ${PID}" EXIT
  fi
  sleep 60
  echo kill $PID
  kill $PID
  sleep 3
  ps -p $PID > /dev/null 2>&1
  EXISTS=$?
  if [ $EXISTS -eq 0 ]; then
	  echo kill -9 $PID
	  kill -9 $PID
  fi
  PID=0
done

