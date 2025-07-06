from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired, FileSize

class UploadImageForm(FlaskForm):
    """画像アップロード用のフォームクラス
    Attributes:
        title: タイトル
        message: メッセージ
        image: アップロードする画像ファイル
        submit: 送信ボタン
 
    """
    # タイトル用のフィールド
    title = StringField(
        "タイトル",
        validators=[DataRequired(), Length(max=200)]
    )
    # メッセージ用のフィールド
    message = TextAreaField(
        "メッセージ",
        validators=[DataRequired(), Length(min=0, max=1000)]
    )
    # 画像ファイル用のフィールド
    image = FileField(
        validators=[
            FileRequired("画像ファイルを選択してくださいｓ"),
            FileAllowed(["jpg", "png", "jpeg", "gif"],"サポートされていないファイル形式です。" )
        ]
    )
    # 送信ボタン用のフィールド
    submit = SubmitField("送信")