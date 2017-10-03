# coding:utf8
# author:dinghai
# created on 2017-10-02 11:03
from enum import Enum

HttpMethod = Enum("HttpMethod", ("GET", "POST",))

MiddlewareType = Enum("MiddlewareType", ("Request", "Response"))


class HttpException(Exception):
    pass


class Request:
    def __init__(self):
        self.method = HttpMethod.GET
        self.cookies = []
        self.form = []
        self.files = []
        self.headers = []
        self.data = ""


class Response:
    pass


if __name__ == "__main__":
    print(HttpMethod.GET)
    print(HttpMethod.POST)
