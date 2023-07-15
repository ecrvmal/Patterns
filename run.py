import os
import sys
from wsgiref.simple_server import make_server
sys.path.append('../')
from framework.processor import Framework
from app.urls import routes
from framework.front_controllersF import fronts


class Run:
    def __init__(self):

        self.application = Framework(routes, fronts)
        with make_server('', 8000, self.application) as httpd:
            print("Serving on port 8000...")
            httpd.serve_forever()


if __name__ == '__main__':
    app = Run()
