import sys
sys.path.append('../')
from framework.templator import render
from framework.engine import Engine, Logger
from framework.request_processing import RequestProcessing
from framework.decor import AppRoute, Timing
from framework.patterns import ListView, CreateView, Serializer, NotifierSMS, NotifierEMAIL, ConsoleWriter



# logger = Logger('views')

engine = Engine()

# routes = {}
logger = Logger('main')
email_notifier = NotifierEMAIL()
sms_notifier = NotifierSMS()


@AppRoute(url='/')
class Index:
    # @Timing(name='Index')
    def __call__(self, request):
        # print(f'   view : cl IndexView  ;              request : {request} ')
        return '200 OK', render('index.html', date=request.get('date'))
        # return '200 OK', render('index.html')


@AppRoute(url='/contacts/')
class ContactsView:
    # @Timing(name='/Contacts/')
    def __call__(self, request):
        # print(f'   view : cl ContactsView;       request : {request} ')
        return '200 OK', render('contacts.html', date=request.get('date'))


@AppRoute(url='/about/')
class AboutView:
    # @Timing(name='/about/')
    def __call__(self, request):
        # print(f'   view : cl ContactsView;       request : {request} ')
        return '200 OK', render('about.html', date=request.get('date'))


# class AdminView:
#     def __call__(self, request):
#         # print(f'   view : about_view  ;         request : {request}  ')
#         return '200 OK', render('admin.html', date=request.get('date'))

@AppRoute(url='/students_list/')
class StudentsListView(ListView):
    queryset = engine.students
    print(f'queryset : {queryset}')
    template_name = 'students_list.html'

@AppRoute(url='/student_create/')
class StudentCreateView(CreateView):
    template_name = 'student_create.html'

    def create_obj(self, data):
        name = data['name']
        name = engine.decode_value(name)
        surname = data['surname']
        surname = engine.decode_value(surname)
        new_student = engine.create_user('student', name, surname)
        engine.students.append(new_student)


@AppRoute(url='/courses_list/')
class CoursesList:
    # @Timing(name='/courses_list/')
    def __call__(self, request):
        logger.log("CoursesList")
        try:
            cat_id = int(request['data']['id'])
            if cat_id > 0:
                cat = engine.find_category_by_id(cat_id)
                return '200 OK', render('course_list.html',
                                        course_list=cat.courses,
                                        name=cat.name, id=cat.cat_id,
                                        date=request.get('date'))
            if cat_id == 0:
                courses = []
                for cat in engine.categories:
                    courses.extend(cat.courses)
                # print(f'courses: {courses}')
                return '200 OK', render('course_list.html',
                                        course_list=courses,
                                        name='All', id=0,
                                        date=request.get('date'))
        except KeyError:
            courses = []
            for cat in engine.categories:
                courses.extend(cat.courses)
            # print(f'courses: {courses}')
            return '200 OK', render('course_list.html',
                                    course_list=courses,
                                    name='All', id=0,
                                    date=request.get('date'))


# @AppRoute(url='/course_create/')
# class CourseCreate:
#     category_id = 0
#
#     # @Timing(name='/course_create/')
#     def __call__(self, request):
#         if request['method'] == "GET":
#             logger.log('course_create Method_get')
#             try:
#                 self.category_id = int(request['data']['id'])
#                 if self.category_id == 0:
#                     return '200 OK', render('course_create.html',
#                                             name='',
#                                             id=1,
#                                             message='Enter to category to create course',
#                                             date=request.get('date'))
#                 else:
#                     # print(f'request : {request}')
#                     # print(f'category_id : {self.category_id}')
#                     category = engine.find_category_by_id(int(self.category_id))
#                     logger.log(
#                         f'course_create Method_get cat_id:{category.id}')
#                     return '200 OK', render('course_create.html',
#                                             name=category.name,
#                                             id=category.id,
#                                             message='',
#                                             date=request.get('date'))
#             except KeyError:
#                 return '200 OK', render('course_create.html',
#                                         name='',
#                                         id=1,
#                                         message='No category has been created yet',
#                                         date=request.get('date'))
#
#         if request['method'] == "POST":
#             logger.log('course_create Method_POST')
#             request_params = request['request_params']
#             print(f'request params : {request_params}')
#             print(f'category_id: {self.category_id}')
#             new_course_name = request_params['course_name']
#             new_course_name = engine.decode_value(new_course_name)
#             existing_course = None
#             try:
#                 existing_course = engine.create_course(new_course_name)
#             except Exception:
#                 pass
#             if not existing_course:
#                 if self.category_id != 0:
#                     category = engine.find_category_by_id(int(self.category_id))
#
#                     course = engine.create_course(
#                         'recorded', new_course_name, category)
#                     engine.courses.append(course)
#                     course.observers.add(email_notifier)
#                     course.observers.add(sms_notifier)
#
#             return '200 OK', render('course_list.html',
#                                     course_list=category.courses,
#                                     name=category.name,
#                                     id=category.id,
#                                     date=request.get('date'))

@AppRoute(url='/course_create/')
class CourseCreate(CreateView):
    template_name = 'course_create.html'
    category_id = 0

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            if self.category_id != 0:
                self.create_obj(data)
                return self.render_template_with_context()

        if request['method'] == 'GET':
            self.category_id = int(request['data']['id'])
            print(f'category_id : {self.category_id}')
            return super().__call__(request)

    def create_obj(self, data):
        course_name = data['course_name']
        course_name = engine.decode_value(course_name)
        category = engine.find_category_by_id(int(self.category_id))
        new_course = engine.create_course('recorded', course_name, category)
        engine.courses.append(new_course)
        new_course.observers.add(email_notifier)
        new_course.observers.add(sms_notifier)


@AppRoute(url='/course_copy/')
class CourseCopy:
    # @Timing(name='/course_copy/')
    def __call__(self, request):
        # print(f'request = {request}')
        logger.log('Course_Copy')
        course_name = request['data']['name']
        try:
            old_course = engine.get_course_by_name(course_name)
        except Exception:
            print(' error during course clone')
        if old_course:
            new_course = old_course.clone()
            new_course.name = f'{old_course.name}_copy'
            engine.courses.append(new_course)
            old_course.category.courses.append(new_course)
            cat = engine.find_category_by_id(old_course.category.id)
            return '200 OK', render('course_list.html',
                                    course_list=cat.courses,
                                    name=cat.name,
                                    id=cat.cat_id,
                                    date=request.get('date'))



@AppRoute(url='/category_list/')
class CategoryList(ListView):
    queryset = engine.categories
    print(f'category queryset : {queryset}')
    template_name = 'category_list.html'


@AppRoute(url='/category_create/')
class CategoryCreate(CreateView):

    template_name = 'category_create.html'

    def create_obj(self, data: dict):
        name = data['category_name']
        name = engine.decode_value(name)
        new_obj = engine.create_category(name)
        engine.categories.append(new_obj)



class PageNotFound404:
    # @Timing(name='/PageNotFound/')
    def __call__(self, request):
        logger.log('PageNotFound404')
        return '404 WHAT', render('page_not_found.html', date=request.get('date'))


@AppRoute(url='student_list')
class StudentListView(ListView):
    queryset = engine.students
    template_name = 'student_list.html'


@AppRoute(url='student_create')
class StudentCreateView(CreateView):
    template_name = 'student_create.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = engine.decode_value(name)
        surname = data['surname']
        surname = engine.decode_value(surname)
        new_obj = engine.create_user('student', name, surname)
        engine.students.append(new_obj)


@AppRoute(url='/student_add/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'student_add.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = engine.courses
        context['students'] = engine.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course_name = engine.decode_value(course_name)
        course = engine.get_course_by_name(course_name)
        student_name = data['student_name']
        student_name = engine.decode_value(student_name)
        student = engine.get_student_by_name(student_name)
        course.add_student(student)


@AppRoute(url='/api/')
class CourseApi:
    # @Timing(name='CourseApi')
    def __call__(self, request):
        return '200 OK', Serializer(engine.courses).save()
