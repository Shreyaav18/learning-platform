from django.urls import path
from .views import course_list_html, course_list_api, course_detail, add_course, enroll_course

urlpatterns = [
    path("", course_list_html, name="course-list-html"),
    path("api/courses/", course_list_api, name="course-list-api"),  # API endpoint
    path("api/courses/<int:pk>/", course_detail, name="course-detail"),  # API detail
    path("add/", add_course, name="add-course"),
    path("enroll/", enroll_course, name="enroll-course"),
]
