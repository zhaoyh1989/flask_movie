import random, string, hashlib, base64

class UserService:

    @staticmethod
    def geneAuthCode(user_info = None):
        m = hashlib.md5()
        tmp_str = f"{user_info.id}-{user_info.login_name}-{user_info.login_salt}"
        m.update(tmp_str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def genePwd(pwd, salt):
        m = hashlib.md5()
        temp_str = f"{base64.encodebytes(pwd.encode('utf-8'))}-{salt}"
        m.update(temp_str.encode("utf-8"))
        return m.hexdigest()

    @staticmethod
    def geneSalt(length = 16):
        saltList = [random.choice((string.ascii_letters + string.digits)) for i in range(length)]
        return "".join(saltList)

