from flask import Blueprint, render_template, session, request
from common.models.movie import Movie
from application import app, logger, db
from common.libs.helper import ops_render, get_pages
from sqlalchemy.sql.expression import func
import math,random

index_page = Blueprint("index_page",__name__)

@index_page.route("/")
def template():
    cur_page = int(request.args.get("p","1"))
    if cur_page < 1:
        cur_page = 1
    page_size = 18
    total_count = Movie.query.count()

    params = {
        "total_count": total_count,
        "page_size" : page_size,
        "cur_page" : cur_page
    }

    page_data = get_pages(params)

    start = (cur_page - 1) * page_size
    end = cur_page * page_size

    movie_infos = Movie.query.order_by(Movie.id.desc())[start:end]
    # movie_infos = None

    logger.info("主页返回逻辑")

    return ops_render("index.html", {"data": movie_infos, "page_data": page_data})

@index_page.route("/info")
def info():
    req = request.args
    id = int(req.get("id"))
    movie_info = Movie.query.filter_by(id=id).first()
    movie_info.view_counter += 1
    db.session.add(movie_info)
    db.session.commit()
    pid = int(req.get("pid"))
    yg = int(req.get("yg"))
    # start = random.randrange(yg-3)
    # 随机取4条记录
    rand_movie = Movie.query.order_by(func.rand()).limit(4)
    data = {
        "movie_info": movie_info,
        "pid": pid,
        "yg": yg,
        "rand_movie": rand_movie
    }

    return ops_render("info.html", data)

