# from app.views import *
from sys import path
path.append('..')
from app.viewsC import *

class Framework:

    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        print(f'environ = {environ}')
        path = environ['PATH_INFO']

        if not path.endswith('/'):
            path = f'{path}/'

        if path in self.routes:
            view = self.routes[path]
        else:
            view = PageNotFound404()

        # ------------------- Front Controller ---------------------#
        # method_list = [func for func in dir(FrontControllers) if callable(getattr(FrontControllers, func))
        #                and not func.startswith("__")]
        # print(f'method_list : {method_list}')

        request = {}
        for front in self.fronts:
            front(request)
        print(request)
        # ------------------- end of Front Controller ---------------------#

        # --------------------   Page Controller --------------------------#
        # code, body = view(request)
        code, body = view(request)
        # --------------------   End of Page Controller --------------------------#

        start_response(code, [('Content-Type', 'text/html')])
        return [body.encode()]
