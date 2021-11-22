# 共用配置
# 日志级别
DEBUG = True
# 屏蔽SQLALCHEMY_TRACK_MODIFICATIONS警告
SQLALCHEMY_TRACK_MODIFICATIONS = False
# 需不需要打印sql
SQLALCHEMY_ECHO = False
# 连接数据库编码
SQLALCHEMY_ENCODING = "utf8mb4"
# 数据库链接配置
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/movie_cat"
# 只有DEBUG为True时才生效，即flask_debugtoolbar才可以用。
SECRET_KEY = "123456xxn"

DOMAIN = {
    "www":"http://192.168.2.106:5000"
}

# RELEASE_PATH = r"D:\workspaces\python\study\Flask\release_version"

# cookie名字
AUTH_COOKIE_NAME = "movie_cat"

