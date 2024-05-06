from django.core.exceptions import ValidationError
from django.core.validators import (
    MaxValueValidator,
    MinValueValidator,
)
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


class Attempt(models.Model):
    quiz = models.ForeignKey(
        Quiz,
        verbose_name='Попытка',
        on_delete=models.CASCADE,
        related_name='attempts',
    )
    attempt_date = models.DateTimeField(
        verbose_name="Дата попытки",
        auto_now_add=True,
        db_index=True,
    )
    result = models.PositiveSmallIntegerField(
        verbose_name='Результат попытки',
        null=True,
        blank=True,
        validators=(
            MinValueValidator(
                limit_value=0,
                message='Результат не может быть меньше 0.',
            ),
            MaxValueValidator(
                limit_value=100,
                message='Результат не может быть больше 100.'
            )
        )
    )

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"
        ordering = ('quiz', '-attempt_date',)

    def __str__(self):
        return f'Попытка №{self.id} "{self.quiz}"'


class Answer(models.Model):
    attempt = models.ForeignKey(
        Attempt,
        verbose_name='Попытка',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    question = models.ForeignKey(
        Question,
        verbose_name='Вопрос',
        on_delete=models.CASCADE,
        related_name='answers',
    )
    given_answer = models.BooleanField(
        verbose_name="Полученный ответ",
        choices=ANSWER_CHOICES,
        null=True,
    )
    is_correct = models.BooleanField(
        verbose_name='Правильный ответ',
        default=False,
    )

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def clean(self):
        """
        Raise ValidationError if the .

        """
        if self.attempt_id is not None and self.question_id is not None:
            attempt = Attempt.objects.get(pk=self.attempt_id)
            quiz = attempt.quiz
            if self.question not in quiz.questions.all():
                raise ValidationError(
                    {'question': 'Этого вопроса нет в тесте.'}
                )

    def save(self, *args, **kwargs):
        """
        Check if the given_answer corresponds to the question correct_answer.

        """
        if self.given_answer == self.question.correct_answer:
            self.is_correct = True
        else:
            self.is_correct = False
        super().save(*args, **kwargs)
