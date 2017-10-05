# coding:utf8
# author:dinghai
# created on 2017-10-02 11:12
from ermiaoweb.core import app
from ermiaoweb.core.app import rend_template
from ermiaoweb.core.http import HttpMethod as method
from ermiaoweb.core.http import MiddlewareType

import json


# application = app.application #部署在uwsgi上需要取消注释，使用自导的服务器则不需要


@app.route('/')
def index(request):
    class P:
        def __init__(self, name, age):
            self.name = name
            self.age = age

    p = P("丁海", 21)
    skills = ["Java", "Python", "Git", "RPC", "分布式"]
    return rend_template('index.html', context_dict={"dinghai": p, "skills": skills})


@app.route('/fileupload', methods=(method.POST,))
def file_handler(request):
    # for file in request.files:
    #     pass

    return "success!"


@app.route('/index', methods=(method.GET, method.POST,))
def test_return_dict(request):
    return {"query_dict": request.query_dict, "cookies": request.cookies, "payoad": request.payload}


@app.route('/test_object')
def test_return_object(request):
    class Person:
        def __init__(self, names, age):
            self.names = names
            self.age = age

    names = request.query_dict.get("name", [''])
    age = request.query_dict.get("age", [0])
    return Person(names, age)


@app.route('/echo')
def test_return_dict_2(request):
    names = request.query_dict.get("name")
    age = request.query_dict.get("age", 0)
    return {"names": names, "age": age}


@app.middleware('/index')
def middleware_index_1(request):
    # print("middleware index 1")
    return True


@app.middleware('/index')
def middleware_index_2(request):
    # print("middleware index 2")
    return True


@app.middleware('/index', methods=(method.GET, method.POST,), http_type=MiddlewareType.Response)
def middleware_index_4(response):
    if isinstance(response, (dict, list,)):
        return json.dumps(response)
    if isinstance(response, object):
        return json.dumps(response.__dict__)


@app.middleware('/echo', methods=(method.POST, method.GET), http_type=MiddlewareType.Request)
def middleware_echo(response):
    # print("middleware echo")
    return True


@app.middleware('/echo', methods=(method.POST, method.GET), http_type=MiddlewareType.Response)
def middleware_echo_response(response):
    # print("middleware_echo_response")
    return True


if __name__ == "__main__":
    # print(http.HttpMethod.GET)
    # print(http.HttpMethod.POST)
    def test_route_register():
        print(app.route_mappings)
        for url, mapping in app.route_mappings.items():
            print(url)
            for item in mapping.items():
                print(item)


    #test_route_register()


    def test_middleware_register():
        print(app.middleware_mapping)
        for type, mapping in app.middleware_mapping.items():
            print(type)
            for url, mapping_2 in mapping.items():
                print(url)
                for method, func in mapping_2.items():
                    print(method, func)


    #test_middleware_register()
    app = app.App()
    app.run()
