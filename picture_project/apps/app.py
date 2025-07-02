"""
初期化処理
"""

from flask import Flask

app = Flask(__name__)
app.config.from_pyfile("setting.py")

""" SQLAlchemyの登録
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)

"""Migrateの登録
"""
from flask_migrate import Migrate

Migrate(app, db)

"""LoginManagerの登録
"""
from flask_login import LoginManager

# LoginManagerのインスタンス生成
login_manager = LoginManager()
# 未ログイン時にリダイレクトするエンドポイントを設定
login_manager.login_view = "index"
# ログインしたときのメッセージを設定
login_manager.login_message = ""
# LoginManagerをアプリに登録する
login_manager.init_app(app)


""" トップページのルーティング
"""
from flask import render_template, url_for, redirect, flash
from apps import models
from apps import forms


@app.route("/", methods=["GET", "POST"])
def index():
    form = forms.SignupForm()
    # サインアップフォームのsubmitボタンが押された時の処理
    if form.validate_on_submit():
        # ユーザーの作成 Userインスタンスの作成
        user = models.User(
            username=form.username.data,
            password=form.password.data,
            email=form.email.data,
        )
        if user.is_duplicate_email():
            flash("登録済みのメールアドレスです")
            return redirect(url_for("index"))  # トップページへリダイレクト

        # ユーザーの登録 DBのテーブルに追加
        db.session.add(user)
        db.session.commit()
        flash("ユーザー登録が完了しました")
        return redirect(url_for("index"))

    return render_template("index.html", form=form)


"""Blueprint authappの登録
"""
# authappのモジュールvies.pyからBlueprint authappをインポート
from apps.authapp.views import authapp

# Flaskオブジェクトにblueprint authappを登録
app.register_blueprint(authapp, url_prefix="/auth")
