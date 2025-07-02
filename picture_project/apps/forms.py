from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    username = StringField(
        "ユーザー名",
        validators=[DataRequired(message="入力が必要です。"), Length(max=30)],
    )

    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="入力が必要です。"),
            Email(message="メールアドレスの形式で入力してください"),
        ],
    )

    password = PasswordField(
        "パスワード",
        validators=[
            DataRequired(message="入力が必要です。"),
            Length(min=8, message="6文字以上で入力してください"),
        ],
    )
    # フォームのsubmitボタン
    submit = SubmitField("新規登録")
