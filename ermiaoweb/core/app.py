# coding:utf8
# author:dinghai
# created on 2017-10-02 11:15
import functools, json
from ermiaoweb.core import http
from wsgiref.simple_server import make_server
from ermiaoweb.utils.tools import *

route_mappings = {}
middleware_mapping = {http.MiddlewareType.Request.name: {}, http.MiddlewareType.Response.name: {}}


# 单例模式
class App(object):
    def __init__(self):
        pass

    def run(self):
        # 解析url,解析request data
        # 调用前置中间件
        # 调用对应的处理函数
        # 调用后置中间件
        # 将设置的响应数据转化为原生的http响应
        httpd = make_server('', 8000, application)
        httpd.serve_forever()


def application(environ, start_response):
    # print(environ)
    # handler = find_matched_handler(environ)
    # before_middleware_list = find_before_middlewares(environ)
    # after_middleware_list = find_after_middlewares(environ)
    #
    # request = parse_request_data(environ)
    # for middleware in before_middleware_list:
    #     if not middleware(request):
    #         break

    # response = handler(request)
    # for middleware in after_middleware_list:
    #     middleware(request)
    # bytes = generate_response(response)
    # bytes = [str(environ).encode("utf8")]

    handler = find_matched_handler(environ, route_mappings)
    request_middleware_list = find_matched_middleware_list(environ, middleware_mapping,
                                                           http_type=http.MiddlewareType.Request)
    response_middleware_list = find_matched_middleware_list(environ, middleware_mapping,
                                                            http_type=http.MiddlewareType.Response)

    request = parse_request_data(environ)
    if not len(request_middleware_list) == 0:
        for middleware_handler in request_middleware_list:
            if not middleware_handler(request):
                start_response('403 Forbidden', [('Content-Type', 'text/html')])
                return [b"ERROR"]

    response = handler(request)

    if not len(request_middleware_list) == 0:
        for middleware_handler in response_middleware_list:
            if not middleware_handler(response):
                start_response('403 Forbidden', [('Content-Type', 'text/html')])
                return [b"ERROR"]

    response_string = generate_response(response)

    bytes = [response_string.encode('utf8')]
    start_response('200 OK', [('Content-Type', 'text/html')])
    return bytes


def route(url, *, methods=(http.HttpMethod.GET,), name=None):
    def wrapper(fun):
        # 注册路由
        method_and_func = {}
        for method in methods:
            method_and_func[method.name] = fun
        route_mappings[url] = method_and_func

        @functools.wraps(fun)
        def decorator(*args, **kwargs):
            __ret = fun(*args, **kwargs)
            return __ret

        return decorator

    return wrapper


def middleware(url, *, methods=(http.HttpMethod.GET,), http_type=http.MiddlewareType.Request):
    # 类似route
    def wrapper(fun):
        # 注册中间件
        for method in methods:
            method_funcs = middleware_mapping[http_type.name].get(url, {})
            func_list = method_funcs.get(method.name, [])
            func_list.append(fun)
            method_funcs[method.name] = func_list
            middleware_mapping[http_type.name][url] = method_funcs

        @functools.wraps(fun)
        def decorator(*args, **kwargs):
            __ret = fun(*args, **kwargs)
            return __ret

        return decorator

    return wrapper
