# coding:utf8
# author:dinghai
# created on 2017-10-02 11:15
import functools, json, os
from ermiaoweb.core import http
from jinja2 import Template
from wsgiref.simple_server import make_server

route_mappings = {}
middleware_mapping = {http.MiddlewareType.Request.name: {}, http.MiddlewareType.Response.name: {}}


class App(object):
    def __init__(self, *, debug=True):
        self.debug = debug

    def run(self):
        httpd = make_server('', 8000, application)
        httpd.serve_forever()


def application(environ, start_response):
    """
    解析url,解析request data
    调用前置中间件
    调用对应的处理函数
    调用后置中间件
    将设置的响应数据转化为原生的http响应
    """
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
            response = middleware_handler(response)

    # response_string = generate_response(response)

    bytes = [response.encode('utf8')]
    start_response('200 OK', [('Content-Type', 'text/html')])
    return bytes


def route(url, *, methods=(http.HttpMethod.GET,)):
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


def middleware(url, *, methods=(http.HttpMethod.GET,), middleware_type=http.MiddlewareType.Request):
    # 类似route
    def wrapper(fun):
        # 注册中间件
        for method in methods:
            method_funcs = middleware_mapping[middleware_type.name].get(url, {})
            func_list = method_funcs.get(method.name, [])
            func_list.append(fun)
            method_funcs[method.name] = func_list
            middleware_mapping[middleware_type.name][url] = method_funcs

        @functools.wraps(fun)
        def decorator(*args, **kwargs):
            __ret = fun(*args, **kwargs)
            return __ret

        return decorator

    return wrapper


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

    request.parse_request_body(environ)
    # request.parse_request_files(environ) #TODO 文件上传：解析multipart/form-data格式数据，有点难

    return request


# def generate_response(response):
#     if isinstance(response, str):
#         return response
#     if isinstance(response, (dict, list,)):
#         return json.dumps(response)
#     if isinstance(response, object):
#         return json.dumps(response.__dict__)


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


def rend_template(path, *, context_dict):
    path = os.path.abspath(path)
    with open(path, 'r') as file:
        html_string = ''
        for line in file.readlines():
            html_string += line
        template = Template(html_string)
        render_string = template.render(context_dict)
    return render_string
