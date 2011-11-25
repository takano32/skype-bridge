#!/bin/bash

export XAUTHORITY=/home/takano32/.Xauthority
export DISPLAY=:16

BRIDGE_PATH=$(cd $(dirname $0);pwd)
BRIDGE_PY=${BRIDGE_PATH}/skype-irc-bridge.py
BRIDGE_CONF=$(pwd)/skype-irc-bridge.conf

if [ ! -f $BRIDGE_CONF ]; then
	echo 'doesnt exist config file'
	exit
fi

PID=0

while :;
do
	ps -p $PID > /dev/null 2>&1
	EXISTS=$?
	if [ $EXISTS -ne 0 ]; then
		echo 'doesnt exist process and bootup'
		LANG=C date
		sudo -u takano32 -E python $BRIDGE_PY &
		PID=$!
		trap "kill ${PID}" EXIT
	fi
	sleep 0.7
done

