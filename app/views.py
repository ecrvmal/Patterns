from framework.templator import render
from framework.engine import Engine, Logger
from framework.request_processing import RequestProcessing

logger = Logger('views')
engine = Engine()

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
        # print(f'   view : cl ContactsView;       request : {request} ')
        return '200 OK', render('about.html', date=request.get('date'))


# class AdminView:
#     def __call__(self, request):
#         # print(f'   view : about_view  ;         request : {request}  ')
#         return '200 OK', render('admin.html', date=request.get('date'))

class CoursesList:
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



class CourseCreate:
    category_id = 0

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

            return '200 OK', render('course_list.html',
                                    course_list=category.courses,
                                    name=category.name,
                                    id=category.id,
                                    date=request.get('date'))





class CourseCopy:
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

class CategoryList:
    def __call__(self, request):
        logger.log('List of Categories')
        return '200 OK', render('category_list.html',
                                cat_list=engine.categories,
                                date=request.get('date'))


class CategoryCreate:
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
    def __call__(self, request):
        logger.log('PageNotFound404')
        return '404 WHAT', render('page_not_found.html', date=request.get('date'))

#
# class Other:
#
#     def __call__(self):
#         return '200 OK', [b'other']
#         return '200 OK', [b'<h1> other </h1>']
