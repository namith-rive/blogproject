import os

# モジュールの親ディレクトリのフルパス
basedir = os.path.dirname(os.path.dirname(__file__))
# 親ディレクトリのblog.sqliteをDB設定
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "blog.sqlite")

# シークレットキーの値は10バイトの文字列をランダム
SECRET_KEY = os.urandom(10)

USERNAME = "admin"
PASSWORD = "abcd1234"
