import os
import sys
from wsgiref.simple_server import make_server
sys.path.append('../')
from framework.framework_processor import Framework
from framework.framework_processor import DebugApplication
from framework.framework_processor import FakeApplication

# from app.views import routes
from framework.decor import routes
from framework.front_controllers import fronts
from pprint import pprint



class RunOperation:
    def __init__(self):
        print('routes:')
        pprint(routes)
        self.application = Framework(routes, fronts)
        with make_server('', 8000, self.application) as httpd:
            print("Serving on port 8000...")
            httpd.serve_forever()

class RunDebug:
    def __init__(self):
        print('routes:')
        pprint(routes)
        self.application = DebugApplication(routes, fronts)
        with make_server('', 8000, self.application) as httpd:
            print("Serving on port 8000...")
            httpd.serve_forever()

class RunFake:
    def __init__(self):
        print('routes:')
        pprint(routes)
        self.application = FakeApplication(routes, fronts)
        with make_server('', 8000, self.application) as httpd:
            print("Serving on port 8000...")
            httpd.serve_forever()


if __name__ == '__main__':
    mode = int(input('Enter mode to run: \n'
                     '1: Operation Mode \n'
                     '2: Debug Mode \n'
                     '3: Fake Mode \n'
                     ':     '))
    if mode == 1:
        app = RunOperation()
    elif mode == 2:
        app = RunDebug()
    elif mode == 3:
        app = RunFake()
    else:
        print('Enter 1...3')
