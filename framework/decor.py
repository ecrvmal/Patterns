from time import time

routes = {}


class AppRoute:

    def __init__(self, url):
        self.url = url

    def __call__(self, cls):
        routes[self.url] = cls()


# --------------------- below is AppRoute decorator as a function / working/ ------------

# def AppRoute( url):
#     """
#     the decoration function (call-back)  builds dict with {url > view.class}  values
#     The decorator builds the dict before the function is calling
#     from here:  https://pythonru.com/osnovy/rukovodstvo-po-dekoratoram-python
#     @param url:
#     @return:
#     """
#     def _approute(func):
#         routes[url] = func()
#         # def wrapped():
#         #     ret = func()
#         #     return ret
#         # return wrapped
#     return _approute



class Timing:
    def __init__(self, name):
        self.name = name

    def __call__(self, func):
        # decorator function is below:
        # print(f'args: {args}')
        # print(f'kwargs: {kwargs}')

        def timeit(*args, **kwargs):

            """
            The timeit function is a decorator that wraps the method it's applied to.
            It prints out how long the wrapped function takes to run, in milliseconds.

            :param *args: Pass a variable number of arguments to a function
            :param **kwargs: Pass keyworded, variable-length argument list to a function
            :return: The result of the function
            :doc-author: Trelent
            """
            start = time()
            result = func(*args, **kwargs)
            delta = time() - start
            print(f'timeit ------------ method {self.name} runs in {delta:2.2f} ms')
            return result

        return timeit

# ------------- below timing decorator as a function /working/ --------------
# def Timing(name):
#     def wrapper(method):
#         def timeit(*args, **kwargs):
#             '''
#             нужен для того, чтобы декоратор класса wrapper обернул в timeit
#             каждый метод декорируемого класса
#             '''
#             start = time()
#             result = method(*args, **kwargs)
#             delta = time() - start
#             print(f'timeit ------------ method {name} runs in {delta:2.2f} ms')
#             return result
#         return timeit
#     return wrapper
