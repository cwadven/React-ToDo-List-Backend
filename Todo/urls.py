from django.urls import path

from Todo.views import ToDoListAPI, CompletedListAPI, ToDoDetailAPI, CompletedDetailAPI, CompletedTodayListAPI, \
    ToDoOrderChangingAPI

urlpatterns = [
    path("", ToDoListAPI.as_view()),
    path("/<int:id>", ToDoDetailAPI.as_view()),
    path("/change-order-number", ToDoOrderChangingAPI.as_view()),
    path("/completed", CompletedListAPI.as_view()),
    path("/completed/today", CompletedTodayListAPI.as_view()),
    path("/completed/<int:id>", CompletedDetailAPI.as_view()),
]