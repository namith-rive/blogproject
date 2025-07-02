from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス",
        validators=[
            DataRequired(message="メールアドレスの入力が必要です"),
            Email(message="メールアドレスの形式で入力してください"),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(message="パスワードの入力が必要です")]
    )
    submit = SubmitField("Login")
