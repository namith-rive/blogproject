import os

# モジュールの親ディレクトリのフルパス
basedir = os.path.dirname(os.path.dirname(__file__))
# 親ディレクトリのblog.sqliteをDB設定
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "blog.sqlite")

# シークレットキーの値は10バイトの文字列をランダム
SECRET_KEY = os.urandom(10)

USERNAME = "admin"
PASSWORD = "abcd1234"


# メール関連の設定-----------------------------------
# GmailのSMTPサーバー
MAIL_SERVER = "smtp.gmail.com"
# メールサーバーのポート番号
MAIL_PORT = 587
# メールサーバーと通信する際にTLS(セキュア)接続を使う
MAIL_USE_TLS = True
# SSLを無効にする
MAIL_USE_SSL = False
# Gmailのメールアドレス
MAIL_USERNAME = "westnamith@gmail.com"
# Gmailのアプリ用パスワード
MAIL_PASSWORD = "mdqo qtzj lxsd fmve"
# 送信元のメールアドレス(Gmailのメールアドレス)
MAIL_DEFAULT_SENDER = "westnamith@gmail.com"
# ---------------------------------------------------
