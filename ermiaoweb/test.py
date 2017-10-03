# coding:utf8
# author:dinghai
# created on 2017-10-02 11:12
from ermiaoweb.core import app
from ermiaoweb.core.http import HttpMethod as method
from ermiaoweb.core.http import MiddlewareType


@app.route('/index', methods=(method.GET, method.POST,))
def index():
    #print("index")
    return "hello world"


@app.route('/echo')
def echo():
    print("echo")



@app.middleware('/index')
def middleware_index(request):
    print("middleware index")


@app.middleware('/echo', methods=(method.POST, method.GET), type=MiddlewareType.Request)
def middleware_echo(response):
    print("middleware echo")


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
