from typing import OrderedDict

from django.db.models import Count, FloatField, Sum
from django.db import DatabaseError, transaction
from rest_framework import serializers

from attempt.models import Answer, Attempt
from quiz.constants import ANSWER_CHOICES
from quiz.models import Question, Quiz


class QuestionSerializer(serializers.ModelSerializer):
    """Serializer for quiz questions."""

    class Meta:
        model = Question
        fields = ('id', 'text')


class QuizSerializer(serializers.ModelSerializer):
    """Serializer for quizzes."""
    questions = QuestionSerializer(read_only=True, many=True)

    class Meta:
        model = Quiz
        fields = ('id', 'title', 'questions')


class AnswerSerializer(serializers.ModelSerializer):
    given_answer = serializers.ChoiceField(choices=ANSWER_CHOICES)

    class Meta:
        model = Answer
        fields = ('id', 'attempt', 'question', 'given_answer', 'is_correct')
        read_only_fields = ('id', 'is_correct', 'attempt')


class AttemptDetailSerializer(serializers.ModelSerializer):
    """Serializer for attempts."""
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Attempt
        fields = ('id', 'quiz', 'attempt_date', 'result', 'answers')
        read_only_fields = ('result',)


class AttemptCreateSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Attempt
        fields = ('id', 'quiz', 'attempt_date', 'result', 'answers')
        read_only_fields = ('id', 'result', 'attempt_date')

    def validate(self, data):
        """Validate that the questions correspond to the quiz."""
        quiz_taken = data['quiz']
        received_answers = data['answers']
        answered_questions = [answer['question'] for answer in received_answers]
        if set(quiz_taken.questions.all()) != set(answered_questions):
            raise serializers.ValidationError(
                'Неверные вопросы или неверный тест.'
            )
        return data

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        try:
            with transaction.atomic():
                attempt = Attempt.objects.create(**validated_data)

                self.__create_answers(attempt, answers)

                attempt.result = self.__get_attempt_result(attempt)
                attempt.save()

        except DatabaseError:
            raise serializers.ValidationError(
                'Произошла ошибка во время выполнения теста.'
            )

        return attempt

    def __create_answers(self, attempt: Attempt, answers: list[OrderedDict]):
        """
        Save Answer instances into db for one attempt.

        """
        for answer in answers:
            is_correct = answer['given_answer'] == answer['question'].correct_answer
            Answer.objects.create(**answer, attempt=attempt, is_correct=is_correct)

    def __get_attempt_result(self, attempt: Attempt) -> float:
        """
        Calculate and return the percentage of correct answers for one attempt
        (the result field for Attempt model).

        """
        right_answers: dict[str, float] = attempt.answers.aggregate(
            result=100 *
            Sum('is_correct', output_field=FloatField()) /
            Count('is_correct', output_field=FloatField()),
        )
        return right_answers['result']
