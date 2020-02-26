# SubwayTraffic Platform
# Description: 
# File: service
# Date: 2020/2/24 - 18:23


class StartException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return "StartError: service start failed. " + self.message
