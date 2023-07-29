# from app.views import *
from pprint import pprint
from sys import path

from vmal_framework.app.views import PageNotFound404
from vmal_framework.framework.templator import render

path.append('../')
from app.views import *
from framework.request_processing import RequestProcessing


class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        # print(f'environ = {environ}')
        route = environ['PATH_INFO']

        if not route.endswith('/'):
            route = f'{route}/'
            # print(f'route = {route}')

        if route in self.routes:
            view = self.routes[route]
            # print(f'view: {view}')
        else:
            view = PageNotFound404()

        request = {}

        # ------------------- Front Controller ---------------------#
        for front in self.fronts:
            front(request)
        # ------------------- end of Front Controller ---------------------#

        # --------------------   Page Controller --------------------------#
        RequestProcessing.get_method(environ, request)
        print(f'method : {request["method"]}       ', end='')
        if request['method'] == 'GET':
            RequestProcessing.process_get_request(environ, request)
            print(f' request_data : {request["data"]}')
        if request['method'] == 'POST':
            RequestProcessing.process_post_request(environ, request)
            print(f'request_params: {request["request_params"]}')

        code, body = view(request)
        # --------------------   End of Page Controller --------------------------#

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode('utf-8')]


# Новый вид WSGI-application.
# Первый — логирующий (такой же, как основной,
# только для каждого запроса выводит информацию
# (тип запроса и параметры) в консоль.
class DebugApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, *args, **kwargs ):
    # def __call__(self, env, start_response):  # these args need to run application
        print('DEBUG MODE')
        print('args')
        pprint(args)

        print('kwargs')
        pprint(kwargs)

        return self.application(*args, **kwargs)    # these args taken from __call__ method
        # return self.application(env, start_response)


# Новый вид WSGI-application.
# Второй — фейковый (на все запросы пользователя отвечает:
# 200 OK, Hello from Fake).
class FakeApplication(Framework):

    def __init__(self, routes_obj, fronts_obj):
        self.application = Framework(routes_obj, fronts_obj)
        super().__init__(routes_obj, fronts_obj)

    def __call__(self, env, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        # return [b'Hi from Fake']
        encoded = render("fake.html").encode("utf-8")
        return [bytes(encoded)]
