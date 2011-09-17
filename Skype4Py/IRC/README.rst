=================
Skype IRC Gateway
=================

skype-irc-bridge.py
===================


必要なモジュール
----------------

- Skype4Py

- python-irclib

Debianでの環境の構築
^^^^^^^^^^^^^^^^^^^^

くらきい
  ららら




VNCサーバとSkypeの起動
----------------------

::

  /usr/bin/dbus-launch /usr/bin/tightvncserver :64
  DISPLAY=:64 nohup /usr/bin/skype

デーモンを起動し続ける
----------------------

- `skype-irc-bridge.sh` スクリプトを実行

チャットルームの識別子を調べる
------------------------------

::

  DISPLAY=:64 python chat_list.py

ToDo
----

- 複数チャンネルに join する仕組みの確認


- 小池にセットアップ方法を教えるときにドキュメントを整備

