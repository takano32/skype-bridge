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

X11またはX11らしい環境でSkypeを起動する
  tightvncserver や Xbvf が使えるはず

::

  $ /usr/bin/dbus-launch /usr/bin/tightvncserver :1

  $ tightvncvewer :1

- python-configobj

- python-irclib

VNCサーバとSkypeの起動
----------------------

::

  /usr/bin/dbus-launch /usr/bin/tightvncserver :16
  DISPLAY=:16

デーモンを起動し続ける
----------------------

- `skype-irc-bridge.sh` スクリプトを実行

チャットルームの識別子を調べる
------------------------------

::

  DISPLAY=:16

ToDo
----

- 複数チャンネルに join する仕組みの確認

- 小池にセットアップ方法を教えるときにドキュメントを整備

  - 自分のアカウントと紐づけて利用するためのオプション

skype_irc_bridge
================

::

  sudo -u www-data python skype_irc_bridge.py 3232

irc_skype_bridge
================

::
  
  python irc_skype_bridge.py tellurium:3232

