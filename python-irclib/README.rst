=============
python-irclib
=============

Skype IRC Gateway
=================

VNCサーバとSkypeの起動
----------------------

::

  sudo su - www-data
  LANG=C XAUTHORITY=/var/www/.Xauthority /usr/bin/dbus-launch tightvncserver :32
  LANG=C XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 nohup /usr/bin/skype

- からwww-dataユーザである必要はない

デーモンを起動し続ける
----------------------

- ToDo

  - `skype-irc-bridge.sh` スクリプトの作成

チャットルームの識別子を調べる
------------------------------

::

  sudo -u www-data  XAUTHORITY=/var/www/.Xauthority DISPLAY=:32 python chat_list.py

ToDo
----

- www-data権限ではなくても動くはず

- 複数チャンネルに join する仕組みの改良

  - nickが重複するので複数のBridgeインスタンスでの解決は難しい

  - チャンネルをリスト化してジョインする

