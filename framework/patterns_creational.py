from copy import deepcopy
from quopri import decodestring
from sqlite3 import connect

# from app.views import engine
from framework.pattern_unit_of_work import DomainObject
from framework.patterns import Subject, FileWriter
# from framework.patterns_db import ObjectMapper


class Singleton(type):

    def __init__(cls, name, bases, attrs, **kwargs):
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        else:
            cls.__instance[name] = super().__call__(*args, **kwargs)
            return cls.__instance[name]


class Logger(metaclass=Singleton):
    def __init__(self, name, writer=FileWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        log_text = f'log --> {text}'
        self.writer.write(log_text)


class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Teacher(User):
    pass


class Student(User, DomainObject):

    def __init__(self, name, surname):
        self.courses = []
        super().__init__(name, surname)

class UserFactory:
    user_types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create_user(cls, user_type, name, surname):
        return cls.user_types[user_type](name, surname)


class CoursePrototype:
    def clone(self):
        return deepcopy(self)


class Course(CoursePrototype, Subject, DomainObject):
    def __init__(self, name, category):
        self.id = None
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'recorded': RecordCourse
    }

    @classmethod
    def create_course(cls, type_, name, category):
        return cls.types[type_](name, category)


class Category(DomainObject):
    cat_id = 0

    def __init__(self,
                 name,
                 # category
                 ):
        Category.cat_id += 1
        self.id = Category.cat_id     # Category.id=0 -> all categories
        self.name = name
        # self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        # if self.category:
        #     result += self.category.course_count()
        return result


class Student2CourseLink(DomainObject):
    def __init__(self, student, course):
        self.id = None
        self.student = student
        self.course = course



class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []
        self.student_2_course_links = []

    @staticmethod
    def create_user(type_, name, surname):
        return UserFactory.create_user(type_, name, surname)
    
    def student_get_by_name(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item

    @staticmethod
    def create_category(name,
                        # category=None,
                        ):
        return Category(name,
                        # category
                        )



    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create_course(type_, name, category)

    def course_get_by_id(self, course_id):
        print(f'searching course #{course_id} ')
        for item in self.courses:
            if item.id == course_id:
                return item
        raise ValueError(f'Course with id {course_id} not found')

    def category_get_by_id(self, cat_id):
        print(f'searching category #{cat_id} ')
        for item in self.categories:
            if item.id == cat_id:
                return item
        raise ValueError(f'Category with id {cat_id} not found')

    def student_get_by_id(self, stud_id):
        print(f'searching student #{stud_id} ')
        for item in self.students:
            if item.id == stud_id:
                return item
        raise ValueError(f'Student with id {cat_id} not found')

    def course_get_by_name(self, course_name):
        print(f'searching course named:{course_name} ')
        for item in self.courses:
            if item.name == course_name:
                return item
        raise ValueError(f'Course with namae {course_name} not found')

    def stud_2_course_link_update(self, stud_id, course_id):
        student = self.student_get_by_id(stud_id)
        course = self.course_get_by_id(course_id)
        course.students.append(student)
        student.courses.append(course)

    @staticmethod
    def student_2_course_link_create(student, course):
        student_2_course_link = Student2CourseLink(student, course)
        return student_2_course_link

    @staticmethod
    def decode_value(str_):
        str_b = bytes(str_.replace('%', '=').replace("+", " "), 'UTF-8')
        str_coded = decodestring(str_b)
        return str_coded.decode('UTF-8')

    def course__get_by_name(self, course_name) -> Course :
        for crs in self.courses:
            if crs.name == course_name:
                return crs

    def courses_get_by_cat_id(self, cat_id):
        result = []
        cat = self.category_get_by_id()
        for crs in self.courses:
            if crs.category == cat:
                result.append(crs)
        return result



connection = connect('framework.sqlite')


class ObjectMapper():
    def __init__(self, connection,
                 # engn,
                 table_name):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = table_name
        # self.engn = engn

    def categories_select_all(self):
        statement = f'SELECT * from categories'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name = item
            obj = Category(name)
            obj.id = id
            result.append(obj)
        return result

    def courses_select_all(self):
        statement = f'SELECT * from courses'
        self.cursor.execute(statement)
        data = self.cursor.fetchall()
        print(f'courses_all data: {data}')
        # result = []
        # if data:
        #     for item in data:
        #         course_id, name, categ_id = item
        #         categ_id = int(categ_id)
        #         # category = category_get_by_id(categ_id)
        #         category = self.engn.category_get_by_id(categ_id)
        #         obj = Course(name, category)
        #         obj.id = course_id
        #         print(f'courses.all: {vars(obj)}')
        #         result.append(obj)
        # return result
        return data

    def students_select_all(self):
        statement = f'SELECT * from students'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, name, surname = item
            student = Student(name, surname)
            student.id = id
            result.append(student)
        return result

    def object_get_by_id(self, id):
        statement = f'SELECT id, name FROM {self.table_name} where id = ?'
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return result
        else:
            raise RecordNotFoundException(f'record with id #{id} not found')

    def get_object_id_by_name(self, obj_name, table_name):
        statement = f'SELECT id, name FROM {table_name} '
        self.cursor.execute(statement, ())
        result = self.cursor.fetchall()
        if result:
            for item in result:
                print(f'get_id_by_name item:{item}')
                if item[1] == obj_name:
                    return item[0]
        else:
            raise RecordNotFoundException(f'Category with name {obj_name} not found')


    def object_insert(self, obj):
        if isinstance(obj, Student):
            statement = f'INSERT INTO {self.table_name} (name, surname) VALUES (?,?)'
            self.cursor.execute(statement, (obj.name, obj.surname))
        elif isinstance(obj, Category):
            statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
            self.cursor.execute(statement, (obj.name,))
        elif isinstance(obj, Course):
            statement = f'INSERT INTO {self.table_name} (name, category_id) VALUES (?,?)'
            self.cursor.execute(statement, (obj.name, obj.category.id))
        elif isinstance(obj, Student2CourseLink):
            statement = f'INSERT INTO {self.table_name} (student_id, course_id) VALUES (?,?)'
            self.cursor.execute(statement, (obj.student.id, obj.course.id))
        else:
            raise ValueError('object to insert to DB is of unknown category')
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def student_insert(self, obj):
        statement = f'INSERT INTO students (name, surname) VALUES (?,?)'
        self.cursor.execute(statement, (obj.name, obj.surname))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def category_insert(self, obj):
        statement = f'INSERT INTO {self.table_name} (name) VALUES (?)'
        self.cursor.execute(statement, (obj.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def course_insert(self, obj):
        statement = f'INSERT INTO {self.table_name} (name, category_id) VALUES (?,?)'
        self.cursor.execute(statement, (obj.name, obj.category.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def object_delete(self, obj):
        statement = f'DELETE FROM {self.table_name} WHERE id=?'
        self.cursor.execute(statement, obj.id)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)



    def student_2_course_link_insert(self, student, course):
        statement = f'INSERT INTO student_2_course (student_id, course_id) VALUES (?,?)'
        self.cursor.execute(statement, (student.id, course.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def student_2_course_links_get_all(self):
        statement = f'SELECT * FROM student_2_course'
        self.cursor.execute(statement, ())
        data = self.cursor.fetchall()
        return data




class MapperRegistry:
    mappers = {
        # 'category': CategoryMapper
        'students': ObjectMapper,
        'categories': ObjectMapper,
        'courses': ObjectMapper,
        'student_2_course_link': ObjectMapper,
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return ObjectMapper(connection,   'students')
            # return ObjectMapper
        if isinstance(obj, Category):
            return ObjectMapper(connection, 'categories')
            # return ObjectMapper
        if isinstance(obj, Course):
            # return ObjectMapper
            return ObjectMapper(connection, 'courses')
        if isinstance(obj, Student2CourseLink):
            # return ObjectMapper
            return ObjectMapper(connection, 'student_2_course')

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'DB Commit Error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'DB Update Error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'DB Delete Error: {message}')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'DB Record Not Found Error: {message}')


            


