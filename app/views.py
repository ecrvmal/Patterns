import sys

from framework.pattern_unit_of_work import UnitOfWork
from framework.patterns_creational import MapperRegistry, ObjectMapper, connection, Course, Student2CourseLink

sys.path.append('../')
from framework.templator import render
from framework.patterns_creational import Engine, Logger, ObjectMapper
from framework.request_processing import RequestProcessing
from framework.decor import AppRoute, Timing
from framework.patterns import ListView, CreateView, Serializer, NotifierSMS, NotifierEMAIL, ConsoleWriter



# logger = Logger('views')

engine = Engine()





# routes = {}
logger = Logger('main')
email_notifier = NotifierEMAIL()
sms_notifier = NotifierSMS()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


mapper = ObjectMapper(connection,
                      # engine,
                      'categories')
engine.categories = mapper.categories_select_all()
print(f'engine.categories: {engine.categories}')

mapper = ObjectMapper(connection,
                      # engine,
                      'courses')
courses_data = mapper.courses_select_all()
if courses_data:
    for item in courses_data:
        course_id, name, categ_id = item
        categ_id = int(categ_id)
        # category = category_get_by_id(categ_id)
        category = engine.category_get_by_id(categ_id)
        obj = Course(name, category)
        obj.id = course_id
        print(f'courses.all: {vars(obj)}')
        engine.courses.append(obj)

print(f'engine.courses: {engine.courses}')

mapper = ObjectMapper(connection,
                      # engine,
                      'students')
engine.students = mapper.students_select_all()
print(f'engine.students: {engine.students}')

mapper = ObjectMapper(connection, 'student_2_courses')
link_data = mapper.student_2_course_links_get_all()
for record in link_data:
    student_id, course_id = record
    student = engine.student_get_by_id(int(student_id))
    course = engine.course_get_by_id(int(course_id))
    course.students.append(student)
    student.courses.append(course)


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
    # queryset = engine.students
    # print(f'queryset : {queryset}')
    template_name = 'students_list.html'
    def get_queryset(self):
        # mapper = MapperRegistry.get_current_mapper('students')
        mapper = ObjectMapper(connection, 'students')
        all_students = mapper.students_select_all()
        engine.students.clear()
        for item in all_students:
            engine.students.append(item)
        return all_students

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
        new_student.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(url='/courses_list/')
class CoursesList:
    # @Timing(name='/courses_list/')
    def __call__(self, request):
        logger.log("CoursesList")
        try:
            cat_id = int(request['data']['id'])
            if cat_id > 0:
                print(f'courses_list request = {request["data"]}')
                print(f'courses_list cat_id: {cat_id}')

                # mapper = ObjectMapper(connection, 'courses')
                # courses_data = mapper.courses_get_by_cat_id(cat_id)
                category = engine.category_get_by_id(cat_id)
                # courses = []
                # for item in courses_data:
                #     c_id, c_name = item
                #     course = Course(c_name, category)
                #     courses.append(course)
                #     engine.courses.append(course)
                #     category.courses.append(course)
                # # cat = engine.find_category_by_id(cat_id)
                print(f'view course list cat.id: {category.id}')
                return '200 OK', render('course_list.html',
                                        course_list=category.courses,
                                        name=category.name, id=category.id,
                                        date=request.get('date'))
            # if cat_id == 0:
            #     courses = []
            #     for cat in engine.categories:
            #         courses.extend(cat.courses)
            #     # print(f'courses: {courses}')
            #     return '200 OK', render('course_list.html',
            #                             course_list=courses,
            #                             name='All', id=0,
            #                             date=request.get('date'))
        except KeyError:
            courses = []
            for cat in engine.categories:
                courses.extend(cat.courses)
            # print(f'courses: {courses}')
            return '200 OK', render('course_list.html',
                                    course_list=courses,
                                    name='All', id=0,
                                    date=request.get('date'))

    # def query_set(self):
    #     mapper = MapperRegistry.get_current_mapper('courses')
    #     return mapper.object_select_all



@AppRoute(url='/course_create/')
class CourseCreate(CreateView):
    template_name = 'course_create.html'
    category_id = 0
    category_obj = None

    def __call__(self, request):
        if request['method'] == 'POST':
            data = self.get_request_data(request)
            if self.category_id != 0:
                self.create_obj(data)
                return self.render_template_with_context()

        if request['method'] == 'GET':
            self.category_id = int(request['data']['id'])
            # category_obj = engine.category_get_by_id(self.category_id)
            print(f'category_id : {self.category_id}')
            return super().__call__(request)

    def create_obj(self, data):
        course_name = data['course_name']
        course_name = engine.decode_value(course_name)
        category = engine.category_get_by_id(int(self.category_id))
        new_course = engine.create_course('recorded', course_name, category)
        engine.courses.append(new_course)
        # engine.categories.courses.append(new_course)
        new_course.observers.add(email_notifier)
        new_course.observers.add(sms_notifier)
        new_course.mark_new()
        UnitOfWork.get_current().commit()


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
            new_course.mark_new()
            UnitOfWork.get_current().commit()
            old_course.category.courses.append(new_course)
            cat = engine.category_get_by_id(old_course.category.id)
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

    # def get_queryset(self):
    #     # mapper = MapperRegistry.get_current_mapper('categories')
    #     mapper = ObjectMapper(connection, 'categories')
    #     all_categories = mapper.object_select_all()
    #     engine.categories.clear()
    #     for item in all_categories:
    #         engine.categories.append(item)
    #         print(f'category : {item.__dir__}')
    #     return all_categories


@AppRoute(url='/category_create/')
class CategoryCreate(CreateView):

    template_name = 'category_create.html'

    def create_obj(self, data: dict):
        name = data['category_name']
        name = engine.decode_value(name)
        new_obj = engine.create_category(name)
        engine.categories.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()



class PageNotFound404:
    # @Timing(name='/PageNotFound/')
    def __call__(self, request):
        logger.log('PageNotFound404')
        return '404 WHAT', render('page_not_found.html', date=request.get('date'))





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
        student = engine.student_get_by_name(student_name)
        course.add_student(student)
        new_link = engine.student_2_course_link_create(student, course)
        engine.student_2_course_links.append(new_link)
        # new_link.mark_new()
        # UnitOfWork.get_current().commit()


@AppRoute(url='/api/')
class CourseApi:
    # @Timing(name='CourseApi')
    def __call__(self, request):
        return '200 OK', Serializer(engine.courses).save()
