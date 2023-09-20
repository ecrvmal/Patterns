from datetime import date


def secret_front(request):

    """
    The secret_front function is a view that returns the secret_front.html template
    with the current date and a secret message.

    :param request: Pass the request object to the function
    :return: None
    :doc-author: Trelent
    """
    request['secret'] = 'some secret'
    request['date'] = date.today()


def other_front(request):

    """
    The other_front function is a view that returns an HttpResponse object.
    It takes one argument, request, which is the HTTP request sent to the server.
    The function then adds a key-value pair to the dictionary of data in
    the request and returns it as an HttpResponse object.

    :param request: Pass the request object to the view
    :return: None
    :doc-author: Trelent
    """
    request['key'] = 'key'


fronts = [secret_front, other_front]


