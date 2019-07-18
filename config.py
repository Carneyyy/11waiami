class Config():
    STATIC_ID = 'http://127.0.0.1:5000/static/'

    GNORE_URLS = ['/api/v1/member/login',
                   '/api/v1/member/cklogin',
                   '/api/v1/food/search',
                   '/api/v1/food/all',
                   '/api/v1/food/info']

    BABEL_DEFAULT_LOCALE = 'zh_Hans_CN'

    SECRET_KEY = 'gebidetaishang'
    # 设置连接数据库的URL
    SQLALCHEMY_DATABASE_URI = 'mysql://root:cs123456@127.0.0.1:3306/11_waimai'

    # 数据库和模型类同步修改
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = True

    APP_ID = 'wx0d3443e4e3934f5c'
    APPSECRET = 'c4609112e6e4918f0bc6c0cd7b08fe41'

    DOMAIN = 'http://127.0.0.1:5000'

    IGNORE_URLS = ['/api/vi/user/login']


# 线上环境
class ProductingConfig(Config):
    DEBUG = False


# 生产环境
class DevelopmentConfig(Config):
    DEBUG = True


mapping_config = {
    'pro': ProductingConfig,
    'dev': DevelopmentConfig,
}
