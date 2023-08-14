

from framework.templator import render
from framework.engine import Engine, Logger
from framework.request_processing import RequestProcessing
from framework.decor import AppRoute, Timing

from framework.patterns import ListView, CreateView, Serializer, NotifierSMS, NotifierEMAIL, ConsoleWriter

# logger = Logger('views')

engine = Engine()

# routes = {}
logger = Logger('main', ConsoleWriter())


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
class StudentsListView:
    queryset = engine.students
    template_name = 'students_list.html'


@AppRoute(url='/courses_list/')
class CoursesList:
    # @Timing(name='/courses_list/')
    def __call__(self, request):
        logger.log("CoursesList")
        try:
            cat_id = int(request['data']['id'])
            if cat_id > 0:
                cat = engine.find_category(cat_id)
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


@AppRoute(url='/course_create/')
class CourseCreate:
    category_id = 0

    # @Timing(name='/course_create/')
    def __call__(self, request):
        if request['method'] == "GET":
            logger.log('course_create Method_get')
            try:
                self.category_id = int(request['data']['id'])
                if self.category_id == 0:
                    return '200 OK', render('course_create.html',
                                            name='',
                                            id=1,
                                            message='Enter to category to create course',
                                            date=request.get('date'))
                else:
                    # print(f'request : {request}')
                    # print(f'category_id : {self.category_id}')
                    category = engine.find_category(int(self.category_id))
                    logger.log(f'course_create Method_get cat_id:{category.id}')
                    return '200 OK', render('course_create.html',
                                            name=category.name,
                                            id=category.id,
                                            message='',
                                            date=request.get('date'))
            except KeyError:
                return '200 OK', render('course_create.html',
                                        name='',
                                        id=1,
                                        message='No category has been created yet',
                                        date=request.get('date'))

        if request['method'] == "POST":
            logger.log('course_create Method_POST')
            request_params = request['request_params']
            print(f'request params : {request_params}')
            print(f'category_id: {self.category_id}')
            new_course_name = request_params['course_name']
            new_course_name = engine.decode_value(new_course_name)
            existing_course = None
            try:
                existing_course = engine.create_course(new_course_name)
            except Exception:
                pass
            if not existing_course:
                if self.category_id != 0:
                    category = engine.find_category(int(self.category_id))

                    course = engine.create_course('recorded', new_course_name, category)
                    engine.courses.append(course)
                    course.observers.append(NotifierSMS)
                    course.observers.append(NotifierEMAIL)


            return '200 OK', render('course_list.html',
                                    course_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    date=request.get('date'))




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
            cat = engine.find_category(old_course.category.id)
            return '200 OK', render('course_list.html',
                                    course_list=cat.courses,
                                    name=cat.name,
                                    id=cat.cat_id,
                                    date=request.get('date'))

@AppRoute(url='/category_list/')
class CategoryList:
    # @Timing(name='/category_list/')
    def __call__(self, request):
        logger.log('List of Categories')
        return '200 OK', render('category_list.html',
                                cat_list=engine.categories,
                                date=request.get('date'))


@AppRoute(url='/category_create/')
class CategoryCreate:

    @Timing(name='/category_create/')
    def __call__(self, request):

        if request['method'] == 'POST':
            logger.log('Category_Create Method POST')
            data = request['request_params']
            name = data['category_name']
            name = engine.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = engine.find_category(int(category_id))

            new_category = engine.create_category(name
                                                  # category
                                                  )

            engine.categories.append(new_category)

            return '200 OK', render('category_list.html',
                                    cat_list=engine.categories,
                                    date=request.get('date'))

        if request['method'] == 'GET':
            logger.log('Category_Create Method GET')
            return '200 OK', render('category_create.html',
                                    categories=engine.categories,
                                    date=request.get('date'))


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
class StudentCreateView:
    template_name = 'student_create.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = engine.decode_value(name)
        surname = data['name']
        surname = engine.decode_value(surname)
        new_obj = engine.create_user('student', name, surname)

@AppRoute(url = '/student_add/')
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
        course = engine.get_course(course_name)
        student_name = data['student_name']
        student_name = engine.decode_value(student_name)
        student_surname = data['student_surname']
        student_surname = engine.decode_value(student_surname)
        student = engine.get_student(student_name)
        course.add_student(student)


@AppRoute(url='/api/')
class CourseApi:
    # @Timing(name='CourseApi')
    def __call__ (self, request):
        return '200 OK', Serializer(engine.courses).save()



