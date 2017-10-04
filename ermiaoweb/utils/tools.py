# coding:utf8
# author:dinghai
# created on 2017-10-03 21:06
import json
from ermiaoweb.core import http


def parse_request_data(environ):
    request = http.Request()
    # request method
    request_method = environ['REQUEST_METHOD']
    request.parse_request_method(request_method)

    # url
    url = environ["PATH_INFO"]
    request.url = url

    # headers
    # TODO header补全
    content_type = environ.get('CONTENT_TYPE', '')
    request.headers["CONTENT_TYPE"] = content_type

    # cookies
    cookies_string = environ.get('HTTP_COOKIE', '')
    request.parse_cookies(cookies_string)

    # url 上的数据
    query_string = environ.get('QUERY_STRING', '')
    request.parse_query_string(query_string)

    # request body
    content_length = 0
    if not environ.get('CONTENT_LENGTH','') == "":
        content_length = int(environ.get('CONTENT_LENGTH'))
    request.content_length = content_length
    wsgi_input = environ.get('wsgi.input')
    request.parse_request_body(wsgi_input)

    return request


def generate_response(response):
    if isinstance(response, str):
        return response
    if isinstance(response, (dict, list,)):
        return json.dumps(response)
    if isinstance(response, object):
        return json.dumps(response.__dict__)


# 根据url以及route_mapping找出匹配的function
def find_matched_handler(environ, route_mappings):
    url = environ.get('PATH_INFO', '/')
    method = environ.get("REQUEST_METHOD", "GET")
    # print(method, url)
    if method == 'GET':
        method = http.HttpMethod.GET
    elif method == 'POST':
        method = http.HttpMethod.POST
    else:
        pass

    try:
        handler = route_mappings[url][method.name]
        # print(handler.__name__)
        return handler

    except KeyError:
        print("no matched handler")


def find_matched_middleware_list(environ, middleware_mapping, http_type=http.MiddlewareType.Request):
    url = environ.get('PATH_INFO', '/')
    method = environ.get("REQUEST_METHOD", "GET")
    # print(method, url)
    if method == 'GET':
        method = http.HttpMethod.GET
    elif method == 'POST':
        method = http.HttpMethod.POST
    else:
        pass

    try:
        middleware_list = middleware_mapping[http_type.name][url][method.name]
        # print(middleware_list)
        return middleware_list
    except KeyError:
        print("no matched middleware")
        return []
