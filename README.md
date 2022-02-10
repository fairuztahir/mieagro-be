# mieagro-be

MIE AGRO Middleware application for Odoo and SAP project with backend service using **Sanic** Python framework, frontend **Vuejs3**, and database **PostgreSQL**

## Prerequisites

The only requirements to build and use this project are **Docker v20.10.10** (or above), **Make** and **Awk**. The latter can easily be substituted with your scripting tool of choice.

For Docker lower than v20.10 you need to enable the BuildKit builder in the Docker CLI. This can be done by setting `DOCKER_BUILDKIT=1` in your environment.

## Index

- [Install](#install)
- [Examples](#examples)

## Install

With a [correctly configured](https://packaging.python.org/en/latest/tutorials/installing-packages/) **Sanic** toolchain in requirements file, you can import a new app dependency library into **Sanic** Framework API backend service. Or add manually in file located at `sanicbe/src/requirements.txt`.

Example to import a new library:

```sh
$ pip install sanic
```

Kindly, go to `docker/` folder for more information.

## Examples

[Sanic API](https://sanicframework.org/en/)

Let's start by adding an API endpoint and handler. To create API's endpoint, you need to add `@app.route()` decorator at the top of the handler function / method. There are 2 parameters to that decorator, first is the endpoint url `"/ping"` and the other one is the type of method `methods=['GET', 'OPTIONS']` to call ping API endpoint. To protect your APIs from public access, you need to add `@protected` decorator at the top of your function. Without it your API endpoint will be exposed and doesn't need an access token when calling the API.

Example to create a Simple keep-alive `/ping` handler.

```py
from sanic.response import json

# Used as K8 health check.
@app.route("/ping", methods=['GET', 'OPTIONS'])
async def ping(request):
  return json({"message": "pong!"})
```

create `ping` logic function inside `src/main.py`. Then add API route decorator endpoint as `/ping`. To return your handler response in **JSON**, import `json` from `sanic.response`. Or, you can import `text` from `sanic.response` to return as a **TEXT** format. To use boilerplate json response structure, import `resJson` method from `helpers.func`. Refer to below code.

```py
from helpers.func import resJson

@app.route("/ping", methods=['GET', 'OPTIONS'])
async def ping(request):
  return resJson(resType.OK, {})
```

Another method is to use **Sanic** router `Blueprint`. In this boilerplate, create your blueprint inside your view controller like an example `GET` request below.

```py
# view controller file
from sanic import Blueprint
from helpers.func import exceptionRaise, resJson

class ExampleController():
  u = Blueprint('example', url_prefix='/')

  @u.get("/example-url")
  @protected
  async def getExample(request):
    try:
      # Logic part here
      ...
      # return response
      return resJson(resType.OK, data, total)
    except:
        exceptionRaise('getUsers')
```

Then, declare your blueprint in `src/application.py` file to group all the existing blueprints into a single route map.

```py
# src/application.py
from views.example import ExampleController

def init_blueprints(app):
    v1_0 = Blueprint.group(
        # declare blueprint here
        ...
        ExampleController.u,
        ...
        url_prefix='/',
        version=1
    )
    app.blueprint(v1_0)
```

send a request using something like:

```sh
$ curl localhost/api/ping -v
```

Expected output would look like below:

```sh
$ curl localhost/api/ping -v
VERBOSE: GET http://localhost/api/ping with 0-byte payload
VERBOSE: received 18-byte response of content type application/json; charset=utf-8


StatusCode        : 200
StatusDescription : OK
Content           : {"message":"pong!"}
RawContent        : HTTP/1.1 200 OK
                    Connection: keep-alive
                    Content-Length: 19
                    Content-Type: application/json; charset=utf-8
                    Date: Wed, 08 Dec 2021 02:09:31 GMT
                    Server: nginx/1.21.4

                    {"message":"pong!"}
Forms             : {}
Headers           : {[Connection, keep-alive], [Content-Length, 19],
                    [Content-Type, application/json; charset=utf-8],
                    [Date, Wed, 08 Dec 2021 02:09:31 GMT]...}
Images            : {}
InputFields       : {}
Links             : {}
ParsedHtml        : mshtml.HTMLDocumentClass
RawContentLength  : 19
```

Logger response from **Docker** running container:

```sh
[2021-12-08 02:09:31 +0000] - (sanic.access)[INFO][172.18.0.7:47448]: GET http://localhost/ping  200 19
```

Example download file in boilerplate, open file at `src/utils/exportcsv.py`, run the command below:

```sh
curl -o your-file-title.csv 'http://localhost/api/v1/download'
```

History record download:

```sh
curl -o your-file-title.csv 'http://localhost/api/v1/download?to_date=2021-11-13'
```

To download as a **TEXT** file

```sh
curl -o your-file-title.txt 'http://localhost/api/v1/download'
```
