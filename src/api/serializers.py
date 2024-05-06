from typing import OrderedDict

from django.db import DatabaseError, transaction
from rest_framework import serializers

from quiz.constants import ANSWER_CHOICES
from quiz.models import Answer, Attempt, Question, Quiz


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
        read_only_fields = ('id', 'result', 'attempt_date', 'quiz')

    def validate_answers(self, data):
        if len(data) < 0:
            raise serializers.ValidationError(
                'Необходимо ответить хотя бы на один вопрос'
            )
        return data

    def create(self, validated_data):
        answers = validated_data.pop('answers')
        try:
            with transaction.atomic():
                attempt = Attempt.objects.create(**validated_data)
                self.__create_answers(attempt, answers)
                attempt.result = self.__get_result(attempt)
                attempt.save()
        except DatabaseError:
            raise serializers.ValidationError(
                "Ошибка"
            )

        return attempt

    def __create_answers(self, attempt: Attempt, answers: list[OrderedDict]):
        for answer in answers:
            is_correct = answer['given_answer'] == answer['question'].correct_answer
            Answer.objects.create(**answer, attempt=attempt, is_correct=is_correct)

    def __get_result(self, attempt: Attempt):
        quiz_questions_count = attempt.quiz.questions.count()
        received_answers = attempt.answers.all()
        correct_answers = received_answers.values_list('is_correct', flat=True)
        result = round(sum(correct_answers) / quiz_questions_count * 100)
        return result
