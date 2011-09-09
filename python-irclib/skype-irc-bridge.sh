#!/bin/sh

export XAUTHORITY=/home/takano32/.Xauthority
export DISPLAY=:64

while :;
do
  ps a | grep '[s]kype-irc-bridge.py' | fgrep 'python' > /dev/null
  EXISTS=$?
  if [ $EXISTS -ne 0 ]; then
    echo 'CRASH!!!!'
    date
    python skype-irc-bridge.py &
  fi
  sleep 5
done

