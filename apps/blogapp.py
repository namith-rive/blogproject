from flask import Flask

# Flaskのインスタンスを生成
app = Flask(__name__)

app.config.from_pyfile("setting.py")

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# flaskオブジェクトを登録
db.init_app(app)

# MigrateオブジェクトにFlaskオブジェクトとSQLAlchemyを登録する
from flask_migrate import Migrate

Migrate(app, db)


"""
トップページのルーティング
"""
from flask import render_template


@app.route("/")
def index():
    # index.htmlをレンダリングして返す
    return render_template("index.html")


"""ブループリントの登録"""
from apps.crud.views import crud

# FlaskオブジェクトにBluprint"crud"を登録する
app.register_blueprint(crud)
