=============
python-irclib
=============

Skype IRC Gateway
=================

skype-irc-bridge.py

VNCサーバとSkypeの起動
----------------------

::

  /usr/bin/dbus-launch /usr/bin/tightvncserver :64
  DISPLAY=:64 nohup /usr/bin/skype

デーモンを起動し続ける
----------------------

- ToDo

  - `skype-irc-bridge.sh` スクリプトの作成

チャットルームの識別子を調べる
------------------------------

::

  DISPLAY=:64 python chat_list.py

ToDo
----

- www-data権限ではなくても動くはず

- 複数チャンネルに join する仕組みの改良

  - nickが重複するので複数のBridgeインスタンスでの解決は難しい

  - チャンネルをリスト化してジョインする

