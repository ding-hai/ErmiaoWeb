# ErmiaoWeb
a python3 web framework based on wsgiref named after my GF
###第三方依赖
1. Jinja2



## Finished
1. 基于装饰器的route注册   初步完成 2017/10/3
2. 请求数据解析 完成url请求数据，form数据,请求体中的文本数据解析初步完成
3. 基于装饰器的中间件[前置中间件与后置中间件] 初步完成 2017/10/4

## TODO
1. 文件上传
2. 模板系统
3. 异常处理机制
4. 文档
5. 牛逼的定位

## Example
```Python
# coding:utf8
# author:dinghai
# created on 2017-10-02 11:12
from ermiaoweb.core import app
from ermiaoweb.core.http import HttpMethod as method
from ermiaoweb.core.http import MiddlewareType

application = app.application #just for uwsig deployment


@app.route('/index', methods=(method.GET, method.POST,))
def test_return_string(request):
    # print("index")
    string_return = ""
    for key, values in request.query_dict.items():
        _temp_str = "%s" % key
        for value in values:
            _temp_str += ": %s " % value
        string_return += _temp_str

    for cookie_name, cookie_value in request.cookies.items():
        print(cookie_name, ":", cookie_value)
    return string_return + "<br>" + str(request.payload) + "<br>" + str(request.cookies)


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
def test_return_dict(request):
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


@app.middleware('/index')
def middleware_index_3(request):
    # print("middleware index 3")
    return True


@app.middleware('/index', methods=(method.GET, method.POST,))
def middleware_index_4(request):
    # print("middleware index 4")
    return True


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


    test_route_register()


    def test_middleware_register():
        print(app.middleware_mapping)
        for type, mapping in app.middleware_mapping.items():
            print(type)
            for url, mapping_2 in mapping.items():
                print(url)
                for method, func in mapping_2.items():
                    print(method, func)


    test_middleware_register()
    app = app.App()
    app.run()

```