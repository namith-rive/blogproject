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
from sqlalchemy import select
from apps import models
from flask import render_template

from flask import request
from flask_paginate import Pagination, get_page_parameter


@app.route("/")
def index():
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())
    # データベースにクエリを発行
    entries = db.session.execute(stmt).scalars().all()

    # 現在のページ番号を取得
    page = request.args.get(get_page_parameter(), type=int, default=1)

    res = entries[(page - 1) * 3 : page * 3]
    # paginateオブジェクトを作成
    pagination = Pagination(page=page, total=len(entries), per_page=3)

    # index.htmlをレンダリングして返す
    # pagomatopmオプションでpaginationオブジェクトを引き渡す
    return render_template("index.html", rows=res, pagination=pagination)


"""問い合わせページのルーティングとビューの定義
フォームデータをメール送信する
"""
from flask import url_for, redirect
from flask import flash
from apps import forms


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = forms.InquiryForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        message = form.message.data
        # メール送信
        send_mail(
            to="westnamith@gmail.com",
            subject="問い合わせページからのメッセージ",
            # template/send_mail.txtをテンプレート指定
            template="send_mail.txt",
            username=username,
            email=email,
            message=message,
        )

        # フラッシュメッセージを取得
        flash("お問い合わせの内容は送信されました")
        return redirect(url_for("contact_complete"))

    return render_template("contact.html", form=form)


"""問い合わせ完了ページのルーティングとビューの定義
"""


@app.route("/contact_complete")
def contact_complete():
    return render_template("contact_complete.html")


"""FlaskインスタンスをMailオブジェクトに登録
"""
from flask_mail import Mail

mail = Mail(app)

from flask_mail import Message


def send_mail(to, subject, template, **kwargs):
    """メールを送信する
    Args:
        to:Mailの送信先
        subject:メールの表題
        template:メール本文に適用するテンプレート
        **kwargs:複数のキーワード引数を辞書として受け取る
    """
    msg = Message(subject, recipients=[to])
    msg.body = render_template(template, **kwargs)
    mail.send(msg)


"""ブループリントの登録"""
from apps.crud.views import crud

# FlaskオブジェクトにBluprint"crud"を登録する
app.register_blueprint(crud)
