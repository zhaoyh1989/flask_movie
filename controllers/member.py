from application import app, db
from flask import Blueprint, render_template, request, session, make_response, redirect
from common.models.user import User
from common.libs.helper import ops_renderJSON
from common.libs.userService import UserService
from common.libs.dataHelper import getCurrentTime
from common.libs.urlManager import UrlManager

member_page = Blueprint("member_page", __name__)


@member_page.route("/reg", methods=["GET", "POST"])
def reg():
    code = 200
    msg = "成功"
    data = {}
    if request.method == "GET":
        return render_template("member/reg.html")
    elif request.method == "POST":
        req = request.values
        login_name = req.get("login_name")
        nickname = req.get("nickname")
        login_pwd = req.get("login_pwd")
        login_pwd2 = req.get("login_pwd2")

        if login_name is None or len(login_name) < 1 or login_pwd is None or len(
                login_pwd) < 6 or login_pwd2 is None or len(login_pwd2) < 6:
            code = 201
            msg = "用户名或密码不符合规定"
            return ops_renderJSON(code=code, msg=msg, data=data)

        if login_pwd2 != login_pwd:
            code = 202
            msg = "确认密码不正确，请检查~"
            return ops_renderJSON(code=code, msg=msg, data=data)

        user_info = User.query.filter_by(login_name=login_name).first()

        if user_info:
            code = 203
            msg = "用户名已存在"
            return ops_renderJSON(code=code, msg=msg, data=data)
        else:
            model_user = User()
            model_user.login_name = login_name
            model_user.nickname = nickname
            model_user.login_salt = UserService.geneSalt(8)
            model_user.login_pwd = UserService.genePwd(login_pwd, model_user.login_salt)
            # app.logger.info("model_user.login_pwd = " + model_user.login_pwd)
            model_user.updated_time = model_user.created_time = getCurrentTime()

            # 向数据库插入数据
            db.session.add(model_user)
            db.session.commit()

            msg = "注册成功~~"
            return ops_renderJSON(code=code, msg=msg, data=data)


@member_page.route("/login", methods=["GET", "POST"])
def login():
    code = 200
    msg = "成功"
    data = {}
    if request.method == "GET":
        return render_template("member/login.html")
    elif request.method == "POST":
        req = request.values
        login_name = req.get("login_name")
        login_pwd = req.get("login_pwd")

        if login_name is None or len(login_name) < 1 or login_pwd is None or len(login_pwd) < 1:
            code = 201
            msg = "用户名或密码错误"
            return ops_renderJSON(code, msg, data)

        # 查询数据库是否有此用户
        user_info = User.query.filter_by(login_name=login_name).first()
        if not user_info:
            code = 301
            msg = "用户名或密码错误"
            return ops_renderJSON(code, msg, data)
        if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
            code = 302
            msg = "用户名或密码错误"
            app.logger.info(UserService.genePwd(login_pwd, user_info.login_salt))
            return ops_renderJSON(code, msg, data)

        if user_info.status != 1:
            code = 303
            msg = "用户状态异常，请联系管理员处理~"
            return ops_renderJSON(code, msg, data)
        msg = "登录成功~"

        # session["uid"] = user_info.id
        resp = make_response(ops_renderJSON(code, msg, data))
        resp.set_cookie(app.config.get("AUTH_COOKIE_NAME"), f"{UserService.geneAuthCode(user_info)}#{user_info.id}",
                        60 * 60 * 24 * 120)
        return resp


@member_page.route("/logout", methods=["GET"])
def logout():
    resp = make_response(redirect(UrlManager.buildUrl("/")))
    resp.delete_cookie(app.config.get("AUTH_COOKIE_NAME"))
    return resp
