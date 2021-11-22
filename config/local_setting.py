from config.base_setting import *
# 本地开发环境配置文件
# 数据库链接配置
SQLALCHEMY_DATABASE_URI = "mysql://root:root@localhost/test"
# 屏蔽SQLALCHEMY_TRACK_MODIFICATIONS警告
SQLALCHEMY_TRACK_MODIFICATIONS = True
# 需不需要打印sql
# SQLALCHEMY_ECHO = True

# 只有DEBUG为True时才生效，即flask_debugtoolbar才可以用。
SECRET_KEY = "xxn123456"

