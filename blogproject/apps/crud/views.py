from flask import Blueprint

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static_crud",
)
# 投稿ページのログイン画面のルーティングとビューの定義
from flask import render_template, url_for, redirect, session
from apps.crud import forms
from apps.blogapp import app


@crud.route("/admincreate", methods=["GET", "POST"])
def login():
    form = forms.AdminForm()
    form.username.data = "admin"
    form.password.data = "abcd1234"

    session["logged_in"] = False

    # ログイン画面のsubmitボタンがクリックされた時の処理
    if form.validate_on_submit():
        if (
            form.username.data != app.config["USERNAME"]
            or form.password.data != app.config["PASSWORD"]
        ):
            # 認証できない場合は再度loginhtmlをレンダリングして、フォームクラスのインスタンスをformに渡す
            return render_template("login.html", form=form)
        else:
            session["logged_in"] = True
            return redirect(url_for("crud.article"))
    # ログイン画面へのアクセスはlogin.htmlをレンダリングしてaDMINfORMのインスタンスFORMを引き渡す
    return render_template("login.html", form=form)


# 投稿ページのルーティングとビュー定義
from apps import models
from apps.blogapp import db


@crud.route("/post", methods=["GET", "POST"])
def article():
    # trueでなければログイン画面にリダイレクト
    if not session.get("logged_in"):
        return redirect(url_for("crud.login"))
    # ArticlePostのインスタンスを生成
    form_art = forms.ArticlePost()
    # submitボタンがクリックされた時の処理
    if form_art.validate_on_submit():
        # モデルクラスBlogpostのインスタンス生成
        blogpost = models.Blogpost(
            title=form_art.post_title.data,
            contents=form_art.post_contents.data,
        )
        # DBに追加
        db.session.add(blogpost)
        # DBにコミット
        db.session.commit()
        # session[logge_in]をNoneにする
        session.pop("logged_in", None)
        # トップページへリダイレクト
        return redirect(url_for("crud.login"))

    # レンダリング
    return render_template("post.html", form=form_art)


"""削除ページログイン画面のルーティングとビューの定義"""


@crud.route("/admindelete", methods=["GET", "POST"])
def login_del():
    form = forms.AdminForm()
    session["logged_in"] = False

    # 削除ページログイン画面のsubmitボタンがクリックされた時の処理
    if form.validate_on_submit():
        # モデルクラスBlogpostのインスタンス生成
        if (
            form.username.data != app.config["USERNAME"]
            or form.password.data != app.config["PASSWORD"]
        ):
            # 認証できない場合は再度login_delete.htmlをレンダリングして、
            # フォームクラスのインスタンスをformに渡す
            return render_template("login_delete.html", form=form)
        else:
            session["logged_in"] = True
            return redirect(url_for("crud.delete_entry"))

    # login_delete.htmlをレンダリングしてAdminFormのインスタンスFormを引き渡す
    return render_template("login_delete.html", form=form)


""" 削除ページのルーティングとビューの定義
"""
from sqlalchemy import select


@crud.route("/delete", methods=["GET", "POST"])
def delete_entry():
    # trueでなければ削除ページログイン画面にリダイレクト
    if not session.get("logged_in"):
        return redirect(url_for("crud.login_del"))

    # データベースクエリを作成
    # レコード全権取得してID値の降順で並べる
    stmt = select(models.Blogpost).order_by(models.Blogpost.id.desc())

    # クエリを発行して結果を取得
    entries = db.session.execute(stmt).scalars().all()

    return render_template("delete.html", entries=entries)


"""
テーブルからレコードを削除する機能のルーティングとビューの定義
"""


@crud.route("/delete/<int:id>")
def delete(id):
    # idのレコードをデータベースから取得
    entry = db.session.get(models.Blogpost, id)

    # 結果を反映する
    db.session.delete(entry)

    # DBにコミット
    db.session.commit()

    # session[logge_in]をNoneにする
    session.pop("logged_in", None)

    # トップページへリダイレクト
    return redirect(url_for("crud.login_del"))
