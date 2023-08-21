from json import dumps, loads

# from framework.patterns_creational import ObjectMapper
from framework.templator import render


class Observer:
    def update(self, subject):
        pass


class Subject:
    def __init__(self):
        self.observers = set()

    def attach(self, observer):
        observer._subject = self
        self.observers.add(observer)

    def notify(self):
        for item in self.observers:
            item.update(self)


class NotifierSMS(Observer):

    def update(self, subject):
        print(f'SMS --> we have new student {subject.students[-1].name}')


class NotifierEMAIL(Observer):

    def update(self, subject):
        print(f'EMAIL -->  we have new student {subject.students[-1].name}')


class Serializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return dumps(self.obj)

    def load(self, data):
        return loads(data)

# --------------------- Templates below ----------------------


class TemplateView:
    template_name = 'template.html'

    def get_context_data(self):
        # context = {'request_data': request['data']}
        # print(f'get_context_data context : {context }')
        return {}

    def get_template(self):
        return self.template_name

    def render_template_with_context(self):
        template_name = self.get_template()
        context = self.get_context_data()
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    queryset = []
    template_name = 'list.html'
    context_object_name = 'objects_list'
    context_message = ''
    context_category = ''

    def get_queryset(self):
        print(f'queryset: {self.queryset}')
        return self.queryset

    def get_context_object_name(self):
        return self.context_object_name

    def get_context_message(self):
        return self.context_message

    def get_context_category(self):
        return self.context_category

    def get_context_data(self):
        queryset = self.get_queryset()
        context_object_name = self.get_context_object_name()
        context_message = self.get_context_message()
        context_category = self.get_context_category()
        context = {context_object_name: queryset}
        context['message'] = ""
        context['category'] = None

        return context


class CreateView(TemplateView):
    template_name = 'create.html'
    message = ''

    def get_request_data(self, request):
        # print(f'request_params : {request["request_params"]}')
        return request['request_params']

    def create_obj(self, data):
        pass

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            self.create_obj(data)

            return self.render_template_with_context()
        if request['method'] == 'GET':
            return super().__call__(request)


class ConsoleWriter:
    def write(self, text):
        print(text)


class FileWriter:
    def __init__(self):
        self.file_name = 'log'

    def write(self, text):
        with open(self.file_name, mode='a', encoding='utf-8') as f:
            f.write(f'{text} \n')
