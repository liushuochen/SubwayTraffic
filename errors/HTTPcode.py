"""
Copyright SubwayTraffic Platform system Development team

Development Time:   2019/11/10
Developer:          LiuShuochen
Effect:             The SubwayTraffic Platform system errors of HTTP.
"""

class STPHTTPException(Exception):
    def __init__(self, message, code):
        self.__message = message
        self.__code = code

    @ property
    def error_message(self):
        return self.__message

    @ error_message.setter
    def error_message(self, message):
        self.__message = message

    @ property
    def httpcode(self):
        return self.__code