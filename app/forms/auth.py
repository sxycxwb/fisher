from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, Email, DataRequired, ValidationError

from app.models.base import db
from app.models.user import User


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField(validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])


class RegisterForm(Form):
    nickname = StringField('昵称', validators=[DataRequired(), Length(2, 10, message='昵称最少需要两个字符，最多10个字符')])
    email = StringField('电子邮件', validators=[DataRequired(), Length(8, 64), Email(message='电子邮箱不符合规范')])
    password = PasswordField('密码', validators=[DataRequired(message='密码不能为空，请输入你的密码'), Length(6, 32)])

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被注册')
