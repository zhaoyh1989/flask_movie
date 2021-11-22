from application import app
from flask import request, g
from common.models.user import User
from common.libs.userService import UserService

@app.before_request
def before_request():
    user_info = check_login()
    g.current_user = None
    if user_info:
        g.current_user = user_info
    # app.logger.info(f"g.current_user = {g.current_user}")
    return

@app.after_request
def after_request(response):
    # app.logger.info("******after_request*********")
    return response

"""
判断用户是否存在
"""
def check_login():
    cookies = request.cookies
    cookies_name = app.config.get("AUTH_COOKIE_NAME")
    auth_cookie = cookies.get(cookies_name)

    if auth_cookie is None:
        return False

    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False

    try:
        user_info = User.query.filter_by(id = auth_info[1]).first()
    except Exception:
        return False

    if user_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(user_info):
        return False

    return user_info

