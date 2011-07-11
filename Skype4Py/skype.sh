#!/bin/bash
XAUTHFILE=/var/run/skype/Xauthority
# XAUTHORITY=$XAUTHFILE xauth add :32 . `mcookie`
# XAUTHORITY=/var/run/skype/Xauthority DISPLAY=:32 vncviewer
XAUTHORITY=$XAUTHFILE sh -c \
  "/usr/bin/xauth add :32 . `mcookie`" && \
XAUTHORITY=$XAUTHFILE sh -c \
  "/usr/bin/Xvfb :32 -screen 0 800x600x8 -nolisten tcp" && \
#sleep 3 && \
#XAUTHORITY=$XAUTHFILE DISPLAY=:32 SKYPE=/usr/bin/skype sh -c \
#  "/usr/bin/nohup $SKYPE &"


sudo su - www-data;LANG=C XAUTHORITY=/var/www/.Xauthority /usr/bin/dbus-launch tightvncserver :32

LANG=C XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 nohup /usr/bin/dbus-launch /usr/bin/skype

while :; do sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 python skype-lingr.py; done

sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 python chat_list.py

sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 vncviewer

