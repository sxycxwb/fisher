from flask import Flask
from flask_login import LoginManager
from app.models.book import db

login_manager = LoginManager()


def create_app():
    app = Flask(__name__)

    # 加载配置文件
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')

    # 注册sqlAlchemy
    db.init_app(app)  # 数据库对象注册flask app核心对象

    # 注册login模块
    login_manager.init_app(app)
    login_manager.login_view = 'web.login'
    login_manager.login_message = '请先登录或注册'

    # 注册蓝图
    register_blueprint(app)

    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.web.book import web
    app.register_blueprint(web)
