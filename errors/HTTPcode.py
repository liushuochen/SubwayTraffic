"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
                    jojoCry
Effect:             The SubwayTraffic Platform system errors of HTTP.
"""

import util


class STPHTTPException(Exception):
    def __init__(self, message, code, stp_code="10000"):
        self.__message = message
        self.__code = code
        self.stp_code = stp_code

    @property
    def error_message(self):
        return self.__message

    @error_message.setter
    def error_message(self, message):
        self.__message = message

    @property
    def httpcode(self):
        return self.__code

    @property
    def tip(self):
        en, zh = util.get_tips(self.stp_code)
        message = {
            "tips_en": en,
            "tips_zh": zh,
            "stp_code": self.stp_code
        }
        return message

    def __str__(self):
        return self.error_message


class DuplicateException(STPHTTPException):
    pass


class DBError(Exception):
    def __init__(self, message, code):
        self.__message = message
        self.__code = code

    @property
    def error_message(self):
        return self.__message

    @error_message.setter
    def error_message(self, message):
        self.__message = message

    @property
    def error_code(self):
        return self.__code

    def __str__(self):
        return self.error_message
