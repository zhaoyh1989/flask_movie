from flask_script import Command
from bs4 import BeautifulSoup
from application import app, db
from common.libs.dataHelper import getCurrentTime
from urllib.parse import urlparse
from common.models.movie import Movie
from common.models.movie_error import MovieError
import requests, os, time, hashlib, json, traceback

"""
执行：
python manager.py runjob -m movie -a list|parse
"""


class JobTask():
    def __init__(self):
        self.source = "ygdy8"
        self.url = {
            "num": 2,
            "url": "https://www.ygdy8.com/html/gndy/dyzz/list_23_#d#.html",
            "path": f"./tmp/{self.source}/"
        }

    """获取电影信息"""

    def run(self, params):
        self.date = getCurrentTime("%Y%m%d")
        act = params["act"]
        if act == "list":
            self.getList()
            self.parseInfo()
        elif act == "parse":
            self.parseInfo()

    """
    获取列表
    """

    def getList(self):
        config = self.url
        path_root = config["path"] + self.date
        path_list = path_root + "/list"
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        self.makeSuredirs(path_root)
        self.makeSuredirs(path_list)
        self.makeSuredirs(path_info)
        self.makeSuredirs(path_json)
        pages = range(1, config["num"] + 1)
        for idx in pages:
            tmp_path = path_list + "/" + str(idx) + ".txt"
            tmp_url = config["url"].replace("#d#", str(idx))
            app.logger.info("get list url = " + tmp_url)
            if os.path.exists(tmp_path):
                app.logger.info(f"已获取第{idx}页内容，跳过。")
                continue
            tmp_content = self.getHttpContent(tmp_url)
            # app.logger.info(tmp_content)
            self.saveContent(tmp_path, tmp_content)
            app.logger.info(f"获取第{idx}页内容完成。")
            time.sleep(0.5)

        for idx in os.listdir(path_list):
            tmp_content = self.getContent(path_list + "/" + str(idx))
            items_data = self.parseList(tmp_content)

            if not items_data:
                continue

            for item in items_data:
                tmp_json_path = path_json + "/" + item["hash"] + ".json"
                tmp_info_path = path_info + "/" + item["hash"] + ".txt"
                if not os.path.exists(tmp_json_path):
                    self.saveContent(tmp_json_path, json.dumps(item, ensure_ascii=False))

                if not os.path.exists(tmp_info_path):
                    tmp_content = self.getHttpContent(item["url"])
                    self.saveContent(tmp_info_path, tmp_content)
                    app.logger.info("已下载：" + item["name"] + ", url = " + item["url"])
                    time.sleep(0.5)

    def parseList(self, content):
        data = []
        config = self.url
        url_info = urlparse(config["url"])
        url_domain = url_info[0] + "://" + url_info[1]
        # app.logger.info(url_domain)
        # app.logger.info(content)
        tmp_soup = BeautifulSoup(str(content), "html.parser")
        tmp_list = tmp_soup.select("div.co_content8 ul table")
        # app.logger.info(tmp_list)
        for tmp_item in tmp_list:
            tmp_target = tmp_item.select("a.ulink")
            tmp_name = tmp_target[0].string
            tmp_name = tmp_name[tmp_name.index("《") + 1:tmp_name.index("》")]
            tmp_href = tmp_target[0]["href"]
            # app.logger.info(tmp_name)
            if not tmp_href.startswith("http"):
                tmp_href = url_domain + tmp_href

            tmp_data = {
                "name": tmp_name,
                "url": tmp_href,
                "hash": hashlib.md5(tmp_href.encode("utf-8")).hexdigest()
            }
            # app.logger.info(tmp_href)
            data.append(tmp_data)

        return data

    def parseInfo(self):
        config = self.url
        path_root = config["path"] + self.date
        path_info = path_root + "/info"
        path_json = path_root + "/json"
        for filename in os.listdir(path_info):
            tmp_json_path = path_json + "/" + filename.split(".")[0] + ".json"
            tmp_info_path = path_info + "/" + filename
            tmp_json_data = json.loads(self.getContent(tmp_json_path), encoding="utf-8")
            # app.logger.info(tmp_json_data["url"])
            tmp_content = self.getContent(tmp_info_path)
            tmp_soup = BeautifulSoup(tmp_content, "html.parser")
            try:
                tmp_info = tmp_soup.select("div#Zoom span")
                tmp_list = str(tmp_info[0]).split("<br/>")
                if len(tmp_list) < 5:
                    tmp_info = tmp_soup.select("div#Zoom span div")
                    tmp_list = []
                    for info in tmp_info:
                        tmp_list.append(info.string)

                # app.logger.info(
                #     "已爬取：" + tmp_json_data["name"] + ", url = " + tmp_json_data["url"] + ", len(tmp_list) = " + str(
                #         len(tmp_list)))
                # app.logger.info(tmp_json_data["hash"])
                # if tmp_json_data["hash"] == "8997825e63427dd3528de9ad4aeb788e":
                #     nu = 0
                #     for itme in tmp_list:
                #         app.logger.info(str(nu) + " " + str(itme))
                #         nu += 1
                # else:
                #     nu = 0
                #     for itme in tmp_list:
                #         app.logger.info(str(nu) + " " + itme)
                #         nu += 1

                tmp_pub_date = tmp_list[self.findIndex(tmp_list, "◎上映日期")]
                # app.logger.info("已爬取：" + tmp_json_data["name"] + ", url = " + tmp_json_data["url"])
                tmp_desc = tmp_list[self.findIndex(tmp_list,"◎简　　介")] + tmp_list[self.findIndex(tmp_list,"◎简　　介")+2]
                # app.logger.info(tmp_desc)
                tmp_classify = tmp_list[self.findIndex(tmp_list,"◎类　　别")]
                tmp_actor = ""
                for ta in tmp_list[self.findIndex(tmp_list,"◎主　　演"):self.findIndex(tmp_list,"◎标　　签")]:
                    tmp_actor = tmp_actor + ", " + ta.lstrip()
                # app.logger.info(tmp_actor)
                tmp_pic_list = tmp_soup.select("div#Zoom span img")
                tmp_pics = []
                for tmp_pic in tmp_pic_list:
                    tmp_pics.append(tmp_pic["src"])
                tmp_download_list = tmp_soup.select("div#Zoom span a")
                tmp_magnet_url = ""
                for tmp_download in tmp_download_list:
                    if tmp_download["href"].startswith("magnet"):
                        tmp_magnet_url = tmp_download["href"]
                        break
                # app.logger.info(tmp_pub_date)
                # app.logger.info(tmp_desc)
                # app.logger.info(tmp_classify)
                # app.logger.info(tmp_actor)
                # app.logger.info(tmp_pics)
                # app.logger.info(tmp_magnet_url)

                tmp_json_data["classify"] = tmp_classify
                tmp_json_data["actor"] = tmp_actor
                if tmp_pics:
                    tmp_json_data["cover_pic"] = tmp_pics[0]
                    tmp_json_data["pics"] = json.dumps(tmp_pics)
                tmp_json_data["desc"] = tmp_desc
                tmp_json_data["magnet_url"] = tmp_magnet_url
                tmp_json_data["pub_date"] = tmp_pub_date
                tmp_json_data["source"] = self.source
                tmp_json_data["view_counter"] = 0
                tmp_json_data["updated_time"] = tmp_json_data["created_time"] = getCurrentTime()

                tmp_movie_info = Movie.query.filter_by(hash=tmp_json_data["hash"]).first()
                if tmp_movie_info:
                    app.logger.info("已存储，跳过：" + tmp_json_data["name"] + ", url = " + tmp_json_data["url"])
                    continue

                tmp_movie_info = Movie(**tmp_json_data)
                # app.logger.info(1111111)
                db.session.add(tmp_movie_info)
                db.session.commit()
                app.logger.info("已爬取：" + tmp_json_data["name"] + ", url = " + tmp_json_data["url"])

            except Exception:
                errMsg = traceback.format_exc()
                tmp_json_data["remarks"] = errMsg
                tmp_movie_error = MovieError(**tmp_json_data)
                db.session.add(tmp_movie_error)
                db.session.commit()
                app.logger.info("失败已记录movie_error表：" + tmp_json_data["name"] + ", url = " + tmp_json_data["url"])

    def findIndex(self,data_list,tag):
        i = 0
        for data in data_list:
            if str(data).startswith(tag):
                return i
            i += 1

    def getContent(self, path):
        # app.logger.info(path)
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as fp:
                return fp.read()
        return ""

    def saveContent(self, path, content):
        if content:
            with open(path, "w", encoding="utf-8") as fp:
                if type(content) != str:
                    content = content.decode("utf-8")
                fp.write(content)
                fp.flush()
                fp.close()

    """获取网页内容"""

    def getHttpContent(self, url):
        try:
            r = requests.get(url)
            if r.status_code != 200:
                return None
            r.encoding = "gbk"
            return r.text
        except Exception:
            return None

    """
    创建目录
    """

    def makeSuredirs(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
