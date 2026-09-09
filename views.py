def submit(request, course_id):

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    user = request.user

    enrollment = Enrollment.objects.get(
        user=user,
        course=course
    )

    submission = Submission.objects.create(
        enrollment=enrollment
    )

    choices = extract_answers(request)

    submission.choices.set(choices)

    submission_id = submission.id

    return HttpResponseRedirect(
        reverse(
            viewname='onlinecourse:exam_result',
            args=(course_id, submission_id)
        )
    )


def extract_answers(request):

    submitted_answers = []

    for key in request.POST:

        if key.startswith('choice'):

            value = request.POST[key]

            choice_id = int(value)

            submitted_answers.append(choice_id)

    return submitted_answers


def show_exam_result(
    request,
    course_id,
    submission_id
):

    context = {}

    course = get_object_or_404(
        Course,
        pk=course_id
    )

    submission = Submission.objects.get(
        id=submission_id
    )

    choices = submission.choices.all()

    total_score = 0

    questions = course.question_set.all()

    for question in questions:

        correct_choices = question.choice_set.filter(
            is_correct=True
        )

        selected_choices = choices.filter(
            question=question
        )

        if set(correct_choices) == set(selected_choices):

            total_score += question.grade

    context['course'] = course

    context['grade'] = total_score

    context['choices'] = choices

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )
