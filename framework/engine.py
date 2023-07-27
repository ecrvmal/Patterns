from copy import deepcopy
from quopri import decodestring


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
    def __init__(self, name):
        self.name = name

    def log(self, text):
        print(f'Logger {self.name} ------ {text}')


class User:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname


class Teacher(User):
    pass


class Student(User):
    pass


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


class Course(CoursePrototype):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)




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


class Category:
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


class Engine:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_, name, surname):
        return UserFactory.create_user(type_, name, surname)

    @staticmethod
    def create_category(name,
                        # category=None,
                        ):
        return Category(name,
                        # category
                        )

    def find_category(self, id_):
        for cat in self.categories:
            if cat.id == id_:
                return cat
        raise ValueError(f'Category with id {id_} not found')

    @staticmethod
    def create_course(type_, name, category):
        return CourseFactory.create_course(type_, name, category)

    @staticmethod
    def decode_value(str_):
        str_b = bytes(str_.replace('%', '=').replace("+", " "), 'UTF-8')
        str_coded = decodestring(str_b)
        return str_coded.decode('UTF-8')

    def get_course_by_name(self, course_name):
        for crs in self.courses:
            if crs.name == course_name:
                return crs


