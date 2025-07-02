from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from apps.app import db


class User(db.Model, UserMixin):
    """モデルクラス
    db.ModelとUserMixinを継承"""

    __tablename__ = "users"
    # 自動連番
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(30), index=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, index=True, nullable=False, unique=True)
    create_at = db.Column(db.DateTime, default=datetime.now)

    @property
    def password(self):
        """passwordプロパティの定義
        Raises:
            AttributeError:読み取り不可
        """
        raise AttributeError("password is not readable")

    @password.setter
    def password(self, password):
        """passwordプロパティのセッター
        トップページのビューにおいてフォームに入力されたパスワードを
        passwordプロパティにセットするときに呼ばれる

        Args:
            password (str): パスワード
        """
        # ハッシュ化したパスワードをpassword_hashフィールドに格納
        self.password_hash = generate_password_hash(password)

    def is_duplicate_email(self):
        """重複チェック
        Returns:ユーザ登録時におけるメールアドレスの重複チェック
            bool: 重複しているかどうか
        """
        # DBからemailカラムの内容がサインインのアドレスと一致するレコードを取得
        # 取得されたらTrue, 取得されない場合はFalseを返す
        return User.query.filter_by(email=self.email).first() is not None
