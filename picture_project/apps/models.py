from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin

# app.pyのdbオブジェクト、login_managerオブジェクト
from apps.app import db, login_manager

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

    def verify_password(self, password):
        """パスワードの照合
        indexビューでログインチェックする際に呼ばれる
        Args:
            password (str): パスワード
        Returns:
            bool: パスワードが正しいかどうか.一致したらTrueを返す
        """
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    """
    Args:
        user_id(str):ユーザーid
    Returns:
        object:対象のユーザのレコード
    """
    return db.session.get(User, user_id)
