from app.views import IndexView, ContactsView, AboutView, \
    CoursesList, CourseCreate, CourseCopy, \
    CategoryList, CategoryCreate



routes = {
    '/': IndexView(),
    '/about/': AboutView(),
    '/contacts/': ContactsView(),
    '/courses_list/': CoursesList(),
    '/course_create/': CourseCreate(),
    '/course_copy/': CourseCopy(),
    '/category_list/': CategoryList(),
    '/category_create/': CategoryCreate(),
    # '/admin/': AdminView(),
    # '/other/': Other(),
}





