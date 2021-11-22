from application import app, db, manager, logger
from flask_script import Server, Command
from jobs.launcher import RunJob
from www import *

# web server
manager.add_command("runserver", Server(host="0.0.0.0", use_debugger=True, use_reloader=True))

# 运行job，会默认运行MovieJob中的run方法。
# from jobs.movie import MovieJob
# manager.add_command("runjob", MovieJob)
manager.add_command("runjob", RunJob)

# create table
@Command
def create_all():
    """创建数据库模型"""
    db.create_all()

manager.add_command("create_all", create_all)

def main():
    manager.run()

if __name__ == '__main__':
    try:
        import sys
        sys.exit(main())
    except Exception as e:
        import traceback
        traceback.print_exc()


