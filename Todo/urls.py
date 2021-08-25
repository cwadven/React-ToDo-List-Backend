from django.urls import path

from Todo.views import ToDoListAPI, CompletedListAPI, ToDoDetailAPI, CompletedDetailAPI

urlpatterns = [
    path("", ToDoListAPI.as_view()),
    path("/<int:id>", ToDoDetailAPI.as_view()),
    path("/completed", CompletedListAPI.as_view()),
    path("/completed/<int:id>", CompletedDetailAPI.as_view()),
]