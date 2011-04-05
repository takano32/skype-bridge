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




sudo -u www-data python skype-lingr.py



