#!/bin/sh

export XAUTHORITY=/var/www/.Xauthority
export DISPLAY=:16

while :;
do
  ps a | grep '[s]kype-lingr.py' |fgrep 'sudo -u www-data -E python' > /dev/null
  EXISTS=$?
  if [ $EXISTS -ne 0 ]; then
    echo 'CRASH!!!!'
    date
    sudo -u www-data -E python skype-lingr.py &
  fi
  sleep 60
done

