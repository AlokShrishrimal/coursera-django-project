from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView

from .models import (
    Course,
    Lesson,
    Instructor,
    Learner,
    Enrollment,
    Question,
    Choice,
    Submission
)


class CourseListView(ListView):
    model = Course
    template_name = 'onlinecourse/course_list_bootstrap.html'
    context_object_name = 'courses'


class CourseDetailView(DetailView):
    model = Course
    template_name = 'onlinecourse/course_detail_bootstrap.html'
    context_object_name = 'course'


def registration_request(request):
    if request.method == 'GET':
        return render(
            request,
            'onlinecourse/registration_bootstrap.html'
        )

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')

        if User.objects.filter(username=username).exists():
            return render(
                request,
                'onlinecourse/registration_bootstrap.html',
                {'error': 'Username already exists.'}
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        login(request, user)

        return HttpResponseRedirect(
            reverse('onlinecourse:index')
        )


def login_request(request):
    if request.method == 'GET':
        return render(
            request,
            'onlinecourse/login_bootstrap.html'
        )

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(
        request,
        username=username,
        password=password
    )

    if user is not None:
        login(request, user)

        return HttpResponseRedirect(
            reverse('onlinecourse:index')
        )

    return render(
        request,
        'onlinecourse/login_bootstrap.html',
        {'error': 'Invalid username or password.'}
    )


def logout_request(request):
    logout(request)

    return HttpResponseRedirect(
        reverse('onlinecourse:index')
    )


def enroll(request, course_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(
            reverse('onlinecourse:login')
        )

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    Enrollment.objects.get_or_create(
        user=request.user,
        course=course
    )

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:course_details',
            args=(course_id,)
        )
    )


# ---------------------------------------------------------
# EXAM SUBMISSION
# ---------------------------------------------------------

def submit(request, course_id):
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    enrollment = get_object_or_404(
        Enrollment,
        user=request.user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    selected_choices = []

    for key in request.POST:
        if key.startswith('choice'):
            choice_id = request.POST[key]

            try:
                choice = Choice.objects.get(
                    id=choice_id
                )

                selected_choices.append(choice)

            except Choice.DoesNotExist:
                pass

    submission.choices.set(
        selected_choices
    )

    return HttpResponseRedirect(
        reverse(
            'onlinecourse:show_exam_result',
            args=(
                course_id,
                submission.id
            )
        )
    )


# ---------------------------------------------------------
# EXAM RESULT
# ---------------------------------------------------------

def show_exam_result(
    request,
    course_id,
    submission_id
):
    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = get_object_or_404(
        Submission,
        pk=submission_id
    )

    score = 0

    questions = course.question_set.all()

    for question in questions:

        correct_choices = set(
            question.choice_set.filter(
                is_correct=True
            )
        )

        selected_choices = set(
            submission.choices.filter(
                question=question
            )
        )

        if correct_choices == selected_choices:
            score += question.grade

    context = {
        'course': course,
        'submission': submission,
        'score': score,
        'questions': questions
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
