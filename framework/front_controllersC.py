class FrontControllers:

    def __init__(self):
        pass

    def secret_front(self):
        def __call__(request):
            request['secret'] = 'some secret'
            # return request

    def other_front(self):
        def __call__(request):
            request['key'] = 'key'
            # return request

    fronts = [secret_front, other_front]


