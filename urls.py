from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'onlinecourse'

urlpatterns = [

    # Home page
    path(
        '',
        views.CourseListView.as_view(),
        name='index'
    ),

    # Course details
    path(
        '<int:pk>/',
        views.CourseDetailView.as_view(),
        name='course_details'
    ),

    # User registration
    path(
        'registration/',
        views.registration_request,
        name='registration'
    ),

    # User login
    path(
        'login/',
        views.login_request,
        name='login'
    ),

    # User logout
    path(
        'logout/',
        views.logout_request,
        name='logout'
    ),

    # Enroll in course
    path(
        '<int:course_id>/enroll/',
        views.enroll,
        name='enroll'
    ),

    # Submit exam
    path(
        '<int:course_id>/submit/',
        views.submit,
        name='submit'
    ),

    # Show exam result
    path(
        'course/<int:course_id>/submission/<int:submission_id>/result/',
        views.show_exam_result,
        name='show_exam_result'
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
