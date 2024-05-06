from django.db.models import Count, F, FloatField, Q, Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import (
    AttemptCreateSerializer,
    AttemptDetailSerializer,
    QuestionSerializer,
    QuizSerializer
)
from quiz.constants import MIN_SUCCESS_SCORE
from quiz.models import Answer, Attempt, Question, Quiz


class QuestionReadOnlyViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all questions. Filter by a quiz id.

    retrieve:
    Return the specific question.

    """
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('quizzes__id',)


class QuizReadOnlyViewset(viewsets.ReadOnlyModelViewSet):
    """
    list:
    Return a list of all quizzes.

    retrieve:
    Return the specific quiz.

    """
    queryset = Quiz.objects.prefetch_related('questions').all()
    serializer_class = QuizSerializer

    @action(methods=['get'], detail=True)
    def report(self, request, *args, **kwargs):
        quiz = self.get_object()
        attempts_count = self.__get_quiz_attempts_num(quiz)
        attempts_success_rate = self.__get_successful_attempts_percent(quiz)

        most_difficult_questions = self.__get_most_difficult_questions(quiz)

        report_data = {
            'number_of_attempts': attempts_count,
            'attempts_success_rate': attempts_success_rate,
            'most_difficult_questions': most_difficult_questions
        }

        return Response(
            status=status.HTTP_200_OK,
            data=report_data,
        )

    def __get_quiz_attempts_num(self, quiz: Quiz) -> int:
        """Return the number of attempts for a particular quiz."""
        return quiz.attempts.count()

    def __get_most_difficult_questions(self, quiz: Quiz) -> list[dict[str, int]]:
        """Return data about the questions which were answered incorrectly the most."""
        quiz_attempt_ids = quiz.attempts.values_list('id', flat=True)

        all_attempts_answers = Answer.objects.filter(attempt__in=quiz_attempt_ids)

        rated_answers = all_attempts_answers.annotate(
            text=F('question__text')
        ).values(
            'question_id', 'text'
        ).annotate(
            score=100 *
            Sum('is_correct', output_field=FloatField()) /
            Count('is_correct', output_field=FloatField()),
        )

        min_score = rated_answers.order_by('score')[0]['score']
        most_difficult_qns = [
            ans for ans in rated_answers if ans['score'] == min_score
        ]

        return most_difficult_qns

    def __get_successful_attempts_percent(self, quiz: Quiz) -> int:
        """
        Calculate and return the percentage of successful attempts
        (with the result field equal or above MIN_SUCCESS_SCORE)
        for one quiz.

        """
        success_percentage: dict[str, int] = quiz.attempts.aggregate(
            percentage=100 *
            Count('id', filter=Q(result__gte=MIN_SUCCESS_SCORE)) /
            Count('id')
        )
        return success_percentage['percentage']


class AttemptViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Attempt.objects.prefetch_related('answers').all()
    serializer_class = AttemptDetailSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('quiz',)

    def get_serializer_class(self):
        if self.action == 'create':
            return AttemptCreateSerializer
        return self.serializer_class
