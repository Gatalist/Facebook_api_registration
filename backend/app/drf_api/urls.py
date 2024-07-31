from django.urls import path
from .views import CreateUserAPIView


urlpatterns = [
    path('v1/createuser/', CreateUserAPIView.as_view()),
]
