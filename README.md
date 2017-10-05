# ErmiaoWeb
a python3 web framework based on wsgiref named after my GF

### 第三方依赖
1. Jinja2
### 安装
pip install ermiaoweb



## Finished
1. 基于装饰器的route注册   初步完成 2017/10/3
2. 请求数据解析 完成url请求数据，form数据,请求体中的文本数据解析初步完成
3. 基于装饰器的中间件[前置中间件与后置中间件] 初步完成 2017/10/4
4. 模板系统
## TODO
1. 文件上传
2. 异常处理机制
3. 文档
4. 牛逼的定位

## Example
```Python
# coding:utf8
# author:dinghai
# created on 2017-10-05 17:10
"""
测试：1.基本路由功能
测试：2.request中间件
测试：3.response中间件
测试：4.模板功能
"""

from ermiaoweb.core import app
from ermiaoweb.core.http import HttpMethod as method
from ermiaoweb.core.http import MiddlewareType as middleware_type
import json


class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age


@app.route('/', methods=(method.GET,))
def index(request):
    name = request.query_dict.get("name", [''])[0]
    p = Person(name, 21)
    skills = ["Java", "Python", "Git", "RPC", "分布式"]
    return app.rend_template('./templates/index.html', context_dict={"dinghai": p, "skills": skills})


@app.middleware('/', methods=(method.GET,), middleware_type=middleware_type.Request)
def request_middleware(request):
    name = request.query_dict.get("name", [''])[0]
    if name == "haibaobao":
        return True
    return False


@app.route('/person')  # methods 默认GET
def get_person(request):
    p = Person("dinghai", 21)
    return p


@app.middleware('/person')  # middleware_type 默认Request
def auth(request):
    name = request.query_dict.get("name", [''])[0]
    if name == "yibaobao":
        return True
    return False


@app.middleware('/person', middleware_type=middleware_type.Response)
def to_json(response):
    return json.dumps(response.__dict__)


server = app.App()
server.run()


```
