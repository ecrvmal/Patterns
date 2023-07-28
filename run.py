import os
import sys
from wsgiref.simple_server import make_server
sys.path.append('../')
from framework.framework_processor import Framework
# from app.views import routes
from framework.decor import routes
from framework.front_controllers import fronts
from pprint import pprint



class Run:
    def __init__(self):
        print('routes:')
        pprint(routes)
        self.application = Framework(routes, fronts)
        with make_server('', 8000, self.application) as httpd:
            print("Serving on port 8000...")
            httpd.serve_forever()


if __name__ == '__main__':
    app = Run()
