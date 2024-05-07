from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from attempt.models import Answer, Attempt


@admin.register(Attempt)
class AttemptAdmin(admin.ModelAdmin):
    """The representation of the Quiz model in the admin interface."""
    list_display = (
        'id',
        'quiz_link',
        'attempt_date',
        'result'
    )

    def quiz_link(self, obj):
        quiz = obj.quiz
        url = reverse('admin:quiz_quiz_changelist') + str(quiz.id)
        return format_html(f'<a href="{url}">{quiz}</a>')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """The representation of the Quiz model in the admin interface."""
    list_display = (
        'id',
        'attempt_link',
        'question',
        'given_answer',
        'is_correct',
    )
    list_filter = ('attempt', 'attempt__quiz')

    def attempt_link(self, obj):
        attempt = obj.attempt
        url = reverse('admin:attempt_attempt_changelist') + str(attempt.id)
        return format_html(f'<a href="{url}">{attempt}</a>')
