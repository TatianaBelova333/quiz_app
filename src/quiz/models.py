from django.db import models

from quiz.constants import ANSWER_CHOICES, TEXT_MAX_LENGTH


class Question(models.Model):
    """Question Model."""
    text = models.CharField(
        verbose_name="Текст вопроса",
        max_length=TEXT_MAX_LENGTH,
        unique=True,
    )
    correct_answer = models.BooleanField(
        verbose_name="Правильный ответ",
        choices=ANSWER_CHOICES,
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.text

    def display_quizzes(self):
        return '; '.join(map(str, self.quizzes.all()))

    display_quizzes.short_description = 'Используются в тестах'


class Quiz(models.Model):
    """Quiz model."""
    title = models.CharField(
        verbose_name='Название теста',
        max_length=TEXT_MAX_LENGTH,
        unique=True,
    )
    questions = models.ManyToManyField(
        Question,
        verbose_name='Вопросы',
        related_name="quizzes",
    )
    created_date = models.DateTimeField(
        verbose_name="Дата создания",
        auto_now_add=True,
    )

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f'Тест "{self.title}"'

    def display_number_of_questions(self):
        return self.questions.count()

    display_number_of_questions.short_description = 'Кол-во вопросов в тесте'
