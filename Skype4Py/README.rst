========
Skype4Py
========

Skype Lingr Gateway
===================

VNCサーバとSkypeの起動
----------------------

::

  sudo su - www-data
  LANG=C XAUTHORITY=/var/www/.Xauthority /usr/bin/dbus-launch tightvncserver :16
  LANG=C XAUTHORITY=/var/www/.Xauthority DISPLAY=:16 nohup /usr/bin/skype

デーモンを起動し続ける
----------------------

::

  sudo su - 
  while :; do date;sudo -u www-data sh -c 'XAUTHORITY=/var/www/.Xauthority DISPLAY=:16 python skype-lingr.py';date; done

現在ではレポジトリに同梱されている `skype-lingr.sh` というスクリプトで常時起動していることを確認しています

チャットルームの識別子を調べる
------------------------------

::

  sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:16 python chat_list.py


