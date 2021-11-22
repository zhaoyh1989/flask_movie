from application import app
from common.libs.dataHelper import getCurrentTime

import os

class UrlManager:
    @staticmethod
    def buildUrl(path):
        config_domain = app.config["DOMAIN"]
        return f"{config_domain['www']}{path}"

    @staticmethod
    def buildStaticUrl(path):
        static_path = "/static"+path+"?ver="+UrlManager.getReleaseVersion()
        return UrlManager.buildUrl(static_path)

    @staticmethod
    def getReleaseVersion():
        """
        版本管理
            开发模式 使用时间戳作为版本号。
            生产模式 使用配置文件进行管理
        :return: 版本号。
        """
        ver = getCurrentTime("%Y%m%d%H%M%S%f")
        release_path = app.config.get("RELEASE_PATH")
        if release_path and os.path.exists(release_path):
            with open(release_path,"r") as fp:
                ver = fp.read()

        return ver

