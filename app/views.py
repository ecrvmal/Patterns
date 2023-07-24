from framework.templator import render


class IndexView:
    def __call__(self, request):
        # print(f'   view : cl IndexView  ;              request : {request} ')
        return '200 OK', render('index.html', date=request.get('date'))
        # return '200 OK', render('index.html')


class ContactsView:
    def __call__(self, request):
        # print(f'   view : cl ContactsView;       request : {request} ')
        return '200 OK', render('contacts.html', date=request.get('date'))


class AboutView:
    def __call__(self, request):
        # print(f'   view : about_view  ;         request : {request}  ')
        return '200 OK', render('about.html', date=request.get('date'))


class PageNotFound404:
    def __call__(self, request):
        return '404 WHAT', render('page_not_found.html', date=request.get('date'))

#
# class Other:
#
#     def __call__(self):
#         return '200 OK', [b'other']
#         return '200 OK', [b'<h1> other </h1>']
