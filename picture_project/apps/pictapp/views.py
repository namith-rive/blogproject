
""" 識別名をpictappにしてBlueprintオブジェクトを生成

    ・テンプレートフォルダーは同じディレクトリの'templates_pict'
    ・staticフォルダーは同じディレクトリの'static_pict'
"""
from flask import Blueprint

pictapp = Blueprint(
    'pictapp',
    __name__,
    template_folder='templates_pict',
    static_folder='static_pict',
    )

"""pictappのトップページのルーティングとビューの定義
"""
from flask import render_template
from flask_login import login_required # login_required
from sqlalchemy import select
from flask import request
from flask_paginate import Pagination, get_page_parameter

# ログイン必須にする
@pictapp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    #投稿画像のレコードをidの降順で全権取得するクエリ
    stmt = select(modelpict.UserPicture).order_by(modelpict.UserPicture.created_at.desc())
    # データベースにクエリ発行
    entries = db.session.execute(stmt).scalars().all()

    # 現在のページ番号を取得
    page = request.args.get(get_page_parameter(), type=int, default=1)

    # entriesから現在のページに表示するレコードを抽出
    res = entries[(page -1)*6: page*6]
    # Paginationオブジェクトを生成
    pagination = Pagination(
        page=page,
        total=len(entries),
        per_page=6
    )
    # top.htmlをレンダリングする
    return render_template('top.html', user_picts=res, pagination=pagination)

"""imagesフォルダー内の画像ファイルのパスを返す機能
"""
from flask import send_from_directory
@pictapp.route('/images/<path:filename>')
def image_file(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'], filename
    )

"""ログアウトのルーティングとビューの定義
"""
from flask_login import logout_user
from flask import render_template, url_for, redirect

@pictapp.route('/logout')
@login_required
def logout():
    # flask_loginのlogout_user()関数でログイン中のユーザーを
    # ログアウトさせる
    logout_user()
    # ログイン画面のindexビューにリダイレクト
    return redirect(url_for('authapp.index'))


""" 画像アップロードページのルーティングとビューの定義
"""
import uuid
from pathlib import Path
from flask_login import login_required, current_user
from flask import current_app

from apps.app import db
from apps.pictapp import forms
from apps.pictapp import models as modelpict

@pictapp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    """ 画像アップロードページの表示
    """
    # フォームクラスのインスタンスを生成
    form = forms.UploadImageForm()
    # フォームの送信があった場合
    if form.validate_on_submit():
        # フォームデータを取得
        file = form.image.data
        # 画像ファイル名から拡張子を取得
        suffix = Path(file.filename).suffix
        # ユニークなファイル名を生成
        filename_uuid = str(uuid.uuid4()) + suffix
        # 画像ファイルのパスを生成
        image_path = Path(
            current_app.config['UPLOAD_FOLDER'], filename_uuid)
        # 画像ファイルを保存

        file.save(image_path)
        # データベースに保存
        upload_data = modelpict.UserPicture(
            # 現在ログイン中のユーザidを格納
            user_id=current_user.id,
            # ログイン中のユーザ名を格納
            title=form.title.data,
            contents=form.message.data,
            image_path=filename_uuid)
        
        # UserPictureオブジェクトをレコードのデータとして、データベースのテーブルに追加
        db.session.add(upload_data)
        # データベースを更新
        db.session.commit()

        # 処理完了後、pictapp.indexにリダイレクト
        return redirect(url_for('pictapp.index'))
    
    # 画像アップロードページへのアクセスはupload.htmlをレンダリングして
    # UploadImageFormのインスタンスformを引き渡す
    return render_template('upload.html', form=form)

@pictapp.route('detail/<int:id>')
@login_required
def show_detail(id):
    detail = db.session.get(modelpict.UserPicture, id)
    return render_template('detail.html', detail=detail)

@pictapp.route('user-list/<int:user_id>')
@login_required
def user_list(user_id):
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.created_at.desc())

    # データベースにクエリ発行
    userlist = db.session.execute(stmt).scalars().all()

    return render_template('userlist.html', userlist=userlist)


"""マイページのルーティングとビューの定義
"""
@pictapp.route('mypage/<int:user_id>')
@login_required
def mypage(user_id):
    stmt = select(
        modelpict.UserPicture).filter_by(user_id=user_id).order_by(
            modelpict.UserPicture.created_at.desc())

    # データベースにクエリ発行
    mylist = db.session.execute(stmt).scalars().all()

    return render_template('mypage.html', mylist=mylist)


"""テーブルからレコードを削除する機能のルーティングとビューの定義
"""
@pictapp.route('delete/<int:id>')
@login_required
def delete(id):
    # 指定されたidのレコードをデータベースから取得
    entry = db.session.get(modelpict.UserPicture, id)

    db.session.delete(entry)
    db.session.commit()

    return redirect(url_for('pictapp.index'))
