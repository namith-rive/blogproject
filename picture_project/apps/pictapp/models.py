from datetime import datetime
# app.pyからdbをインポート
from apps.app import db

class UserPicture(db.Model):
    """picuresテーブルのモデルクラス
    db.Modelを継承してモデルクラスを定義
    """
    # テーブル名を指定
    __tablename__ = 'pictures'
    # テーブルのカラムを定義
    id = db.Column(
        db.Integer, 
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.String,
        db.ForeignKey('users.id')
    )
    # ユーザ名用のフィールド
    username = db.Column(db.String, index=True)

    # タイトル用のフォール度
    title = db.Column(db.String)

    # 本文用のフィールド
    contents = db.Column(db.Text)
    
    # 画像ファイルのパス用のフィールド
    image_path = db.Column(
        db.String)
    
    # 作成日時用のフィールド
    created_at = db.Column(
        db.DateTime, 
        default=datetime.now)
    