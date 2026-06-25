from django.urls import path
from . import views

app_name = 'flashcards'

urlpatterns = [
    path('', views.flashcard_view, name='flashcard_view'),
]
