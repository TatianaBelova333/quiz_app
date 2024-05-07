from django.contrib import admin

from quiz.models import Question, Quiz


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """The representation of the Question model in the admin interface."""
    list_display = (
        'id',
        'text',
        'correct_answer',
        'display_quizzes',
    )
    ordering = ('pk',)
    list_filter = ('quizzes__title',)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """The representation of the Quiz model in the admin interface."""
    list_display = (
        'id',
        'title',
        'created_date',
        'display_number_of_questions',
    )
