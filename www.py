from application import app
from controllers.indexControllers import index_page
from controllers.member import member_page
from flask_debugtoolbar import DebugToolbarExtension
"""拦截器处理 和 错误处理器"""
from interceptors.auth import *
from interceptors.error import *

# 打开flask_debugtoolbar工具
# toolbar = DebugToolbarExtension(app)

app.register_blueprint(index_page,url_prefix="/")
app.register_blueprint(member_page,url_prefix="/member")

"""模板函数"""
from common.libs.urlManager import UrlManager
app.add_template_global(UrlManager.buildUrl, "buildUrl")
app.add_template_global(UrlManager.buildStaticUrl, "buildStaticUrl")

