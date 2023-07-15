
def index_view(request):
    print(f'   view : Index  ;              request : {request} ')
    return '200 OK', [b'Index']


def contacts_view(request):
    print(f'   view : contacts_view ;       request : {request} ')
    return '200 OK', [b'Contacts page']


def about_view(request):
    print(f'   view : about_view  ;         request : {request}  ')
    return '200 OK', [b'about_page']


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'

#
# class Other:
#
#     def __call__(self):
#         return '200 OK', [b'other']
#         return '200 OK', [b'<h1> other </h1>']
