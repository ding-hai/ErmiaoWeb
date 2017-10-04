# coding:utf8
# author:dinghai
# created on 2017-10-02 11:03
from enum import Enum
from urllib.parse import parse_qs

HttpMethod = Enum("HttpMethod", ("GET", "POST",))

MiddlewareType = Enum("MiddlewareType", ("Request", "Response"))


class HttpException(Exception):
    pass


class Request:
    def __init__(self, *, content_length=0, url=None, cookies=None, query_dict=None, form_dict=None, payload=None,
                 method=HttpMethod.GET):
        self.url = url
        self.method = method
        self.cookies = cookies
        self.headers = {}
        self.form = form_dict
        self.query_dict = query_dict
        self.files = []  # TODO 文件上传支持
        self.payload = payload
        self.content_length = content_length

    def parse_cookies(self, cookies_string):
        cookies_dict = {}
        if not cookies_string == '':
            cookies_array = cookies_string.split(";")
            for cookie in cookies_array:
                name_value_pairs = cookie.split("=")
                name = name_value_pairs[0]
                value = name_value_pairs[1]
                if name not in cookies_dict.keys():
                    cookies_dict[name] = value
        self.cookies = cookies_dict

    def parse_query_string(self, query_string):
        query_dict = {}
        if not query_string == '':
            query_dict = parse_qs(query_string)
        self.query_dict = query_dict

    def parse_request_method(self, request_method_string):
        if request_method_string == 'GET':
            self.method = HttpMethod.GET
        elif request_method_string == 'POST':
            self.method = HttpMethod.POST
        else:
            self.method = HttpMethod.GET

    def parse_request_body(self, wsgi_input):
        request_body = wsgi_input.read(self.content_length).decode('UTF8')
        content_type = self.headers['CONTENT_TYPE']
        payload = {}
        if content_type == 'application/x-www-form-urlencoded':
            payload = parse_qs(request_body)
        elif content_type == 'application/json':
            payload = json.loads(request_body)

        self.payload = payload


# TODO response面向对象
class Response:
    pass


# TODO Cookie设置
class Cookie(object):
    def __init__(self, name, value, expires=10):
        self.name = name
        self.value = value
        self.expires = expires
        self.domain = ""
        self.path = ""
        self.secure = ""


if __name__ == "__main__":
    print(HttpMethod.GET)
    print(HttpMethod.POST)
