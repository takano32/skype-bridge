#----
sudo su - www-data
LANG=C XAUTHORITY=/var/www/.Xauthority /usr/bin/dbus-launch tightvncserver :32
LANG=C XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 nohup /usr/bin/skype
#----

sudo su - 
while :; do date;sudo -u www-data sh -c 'XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 python skype-lingr.py';date; done

sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 python chat_list.py


