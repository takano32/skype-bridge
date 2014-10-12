#!/bin/sh

# export XAUTHORITY=/var/www/.Xauthority
export DISPLAY=:64

while :;
do
  ps a | grep '[s]kype-lingr.py' |fgrep 'python' > /dev/null
  EXISTS=$?
  if [ $EXISTS -ne 0 ]; then
    echo 'CRASH!!!!'
    date
    python skype-lingr.py &
  fi
  sleep 1
done

