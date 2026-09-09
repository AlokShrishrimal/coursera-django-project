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

            choice = Choice.objects.get(
                id=choice_id
            )

            selected_choices.append(choice)

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

    for question in course.question_set.all():

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
        'score': score
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
