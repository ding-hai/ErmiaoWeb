# coding:utf8
# author:dinghai
# created on 2017-10-02 11:15
import functools, json
from ermiaoweb.core import http
from wsgiref.simple_server import make_server

route_mappings = {}
middleware_mapping = {http.MiddlewareType.Request: {}, http.MiddlewareType.Response: {}}


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

        def application(environ, start_response):
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

            handler = find_matched_handler(environ)
            request = parse_request_data(environ)
            response = handler(request)

            response_string = generate_response(response)
            bytes = [response_string.encode('utf8')]
            start_response('200 OK', [('Content-Type', 'text/html')])
            return bytes

        def parse_request_data(environ):
            request = http.Request()
            # request method
            request_method = environ['REQUEST_METHOD']
            request.parse_request_method(request_method)

            # url
            url = environ["PATH_INFO"]
            request.url = url

            # headers
            # TODO
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
            if not environ.get('CONTENT_LENGTH') == "":
                content_length = int(environ.get('CONTENT_LENGTH'))
            request.content_length = content_length
            wsgi_input = environ.get('wsgi.input')
            request.parse_request_body(wsgi_input)

            return request

        def generate_response(response):
            if isinstance(response, str):
                return response.encode('utf8')
            if isinstance(response, (dict, list,)):
                return json.dumps(response)
            if isinstance(response, object):
                return json.dumps(response.__dict__)

        # 根据url以及route_mapping找出匹配的function
        def find_matched_handler(environ):
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

        def find_before_middlewares(environ):
            return ""

        def find_after_middlewares(environ):
            return ""

        def parse_cookies(cookies_string):
            cookies_dict = {}
            cookies_array = cookies_string.split(";")
            for cookie in cookies_array:
                name_value_pairs = cookie.split("=")
                name = name_value_pairs[0]
                value = name_value_pairs[1]
                if name not in cookies_dict.keys():
                    cookies_dict[name] = value
            return cookies_dict

        httpd = make_server('', 8000, application)
        httpd.serve_forever()


def route(url, *, methods=(http.HttpMethod.GET,), name=None):
    """
    :param url:
    :param methods:
    :return:
    :function:添加url和处理函数到route_mapping
    """

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


def middleware(url, *, methods=(http.HttpMethod.GET,), type=http.MiddlewareType.Request):
    # 类似route
    def wrapper(fun):
        # 注册中间件
        method_and_func = {}
        for method in methods:
            method_and_func[method.name] = fun

        middleware_mapping[type][url] = method_and_func

        @functools.wraps(fun)
        def decorator(*args, **kwargs):
            __ret = fun(*args, **kwargs)
            return __ret

        return decorator

    return wrapper


def pasrse_request():
    pass
