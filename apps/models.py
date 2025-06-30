from datetime import datetime
from apps.blogapp import db


class Blogpost(db.Model):
    __tablename__ = "posted"

    # 連案を自動でフルフィールド、プライマリーキー
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # タイトル用のフィールド
    title = db.Column(db.String(200), nullable=False)
    # 本文用のフィールド
    contents = db.Column(db.Text, nullable=False)
    # 投稿日のフィールド
    create_at = db.Column(db.Date, default=datetime.today())
