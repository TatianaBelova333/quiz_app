from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from api.serializers import (
    AttemptCreateSerializer,
    AttemptDetailSerializer,
    QuestionSerializer,
    QuizSerializer
)
from quiz.models import Question, Quiz


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
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class AttemptViewset(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = AttemptDetailSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return AttemptCreateSerializer
        return self.serializer_class

    def _get_quiz(self):
        quiz_id = self.kwargs.get('quiz_pk')
        return get_object_or_404(Quiz, pk=quiz_id)

    def get_queryset(self, *args, **kwargs):
        quiz = self._get_quiz()
        return quiz.attempts.all()

    def perform_create(self, serializer):
        quiz = self._get_quiz()
        serializer.save(quiz=quiz)
