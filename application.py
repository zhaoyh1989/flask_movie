from flask import Flask
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os, logging

app = Flask(__name__)
manager = Manager(app)
app.config.from_pyfile("config/base_setting.py")
# 设置ops_config=local|production|test
"""
设置环境变量。
linux:  export ops_config=local|production|test
windows:  set ops_config=local|production|test
"""
if "ops_config" in os.environ:
    app.logger.error(f"加载配置文件：config/{os.environ['ops_config']}_setting.py")
    app.config.from_pyfile(f"config/{os.environ['ops_config']}_setting.py")

db = SQLAlchemy(app)

logging.basicConfig(
    # filename="./filedir/test.log",
    format="%(asctime)s %(levelname)s %(filename)s %(lineno)s: %(message)s",
    # datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG
)

logger = logging.getLogger(__name__)

