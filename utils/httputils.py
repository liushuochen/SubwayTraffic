# SubwayTraffic Platform
# Description: 
# File: httputils
# Date: 2020/1/9 - 22:04


def single(cls):
    instance_dict = {}

    def filter(*args, **kwargs):
        if cls not in instance_dict:
            instance_dict[cls] = cls(*args, **kwargs)
        return instance_dict[cls]

    return filter


@single
class __HttpUtils(object):
    def __init__(self):
        self.OK = 200
        self.Created = 201
        self.Accepted = 202
        self.ResetContent = 205
        self.BadRequest = 400
        self.Unauthorized = 401
        self.Forbidden = 403
        self.NotFound = 404
        self.MethodNotAllowed = 405
        self.NotAcceptable = 406
        self.InternalServerError = 500


http_code = __HttpUtils()
