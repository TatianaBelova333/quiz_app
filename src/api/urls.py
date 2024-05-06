from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import AttemptViewset, QuestionReadOnlyViewset, QuizReadOnlyViewset

app_name = 'api'

router_v1 = DefaultRouter()

router_v1.register(
    'questions', QuestionReadOnlyViewset, basename='questions',
)
router_v1.register(
    'quizzes', QuizReadOnlyViewset, basename='quizzes',
)
router_v1.register(
    'attempts', AttemptViewset, basename='attempts',
)

urlpatterns = [
    path('', include(router_v1.urls)),
]
