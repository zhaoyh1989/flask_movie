from flask import jsonify, g, render_template
from application import logger
import math

def ops_renderJSON(code = 200, msg = "成功", data={}):
    resp = {"code":code, "msg":msg, "data":data}
    return jsonify(resp)

def ops_render(template, context = {}):
    if "current_user" in g:
        context["current_user"] = g.current_user

    logger.info(context)

    return render_template(template, **context)

def get_pages(params):
    total_count = params["total_count"]
    page_size = params["page_size"]
    cur_page = params["cur_page"]

    total_pages = math.ceil(total_count / page_size)
    if total_pages == 0:
        total_pages = 1

    # 控制分页栏中间数量
    if cur_page <= 5:
        lstart = 1
        lend = 10
    elif cur_page >= total_pages - 4:
        lstart = total_pages - 8
        lend = total_pages + 1
    else:
        lstart = cur_page - 4
        lend = cur_page + 5
    # 控制首页和上一页是否可以点击
    lflag = 1
    if cur_page <= 1:
        lflag = 0

    rflag = 1
    if cur_page >= total_pages:
        rflag = 0

    page_data = {
        "page_size": page_size,
        "total_count": total_count,
        "total_pages": total_pages,
        "range": range(lstart, lend),
        "cur_page": cur_page,
        "lflag": lflag,
        "rflag": rflag
    }
    return page_data

