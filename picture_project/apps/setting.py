import os

# 親ディレクトリのフルパスを取得
basedir = os.path.dirname(os.path.dirname(__file__))
# 親ディレクトリのpict.sqliteをデータベースに設定
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.sqlite")

# シークレットキーの値として１０バイト文字列をランダムに生成
SECRET_KEY = os.urandom(10)
