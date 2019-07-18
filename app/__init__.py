from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import time
from flask import logging
from flask_admin import Admin
from flask_login import LoginManager
import pymysql
pymysql.install_as_MySQLdb()
db = SQLAlchemy()

login_manager = LoginManager()
login_manager.login_view = 'admin.login'
app = None
# 简单工厂
def createApp(config):
    global app
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    #国际化
    from flask_babel import Babel
    Babel(app)

    #绑定app
    login_manager.init_app(app)

    # 注册蓝图
    # from app.api.v1 import createBluePrint
    # app.register_blueprint(createBluePrint(), url_prefix='/api/v1')


    #管理后台的蓝图
    # from app.admin import admin_page
    # app.register_blueprint(admin_page,url_prefix='/admin')
    # admin = Admin(app,name='env manager')
    adm = Admin(app, name="订餐管理系统", template_mode='bootstrap3', base_template='admin/mybase.html')

    from app.models.member import Member
    from app.models.admin import User  # 管理员模型类
    from app.models.food import Category, Food  # 管理员模型类
    from app.admin.modelview import MyModelView, UModelview, FModelview
    adm.add_view(UModelview(User, db.session, name='管理员管理'))
    adm.add_view(MyModelView(Member, db.session, name='会员管理'))
    adm.add_view(MyModelView(Category, db.session, name='分类管理'))
    adm.add_view(FModelview(Food, db.session, name='食品管理'))

    # 初始化日志
    # app.logger.addHandler(initlog())
    return app


def initlog():
    log_dir_name = "app/logs"
    log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.log'
    log_file_str = log_dir_name + os.sep + log_file_name
    log_level = logging.DEBUG
    handler = logging.FileHandler(log_file_str, encoding='UTF-8')
    handler.setLevel(log_level)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(message)s')
    handler.setFormatter(logging_format)
    return handler