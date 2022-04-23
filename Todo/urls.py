from django.urls import path

from Todo.views import (
    ToDoListAPI,
    ToDoDetailAPI,
    ToDoOrderChangingAPI,
    CompletedListAPI,
    CompletedDetailAPI,
    CompletedTodayListAPI,
    CategoryListAPI,
    CategoryDetailAPI,
    CategoryOrderChangingAPI,
)

urlpatterns = [
    path("", ToDoListAPI.as_view()),
    path("/category", CategoryListAPI.as_view()),
    path("/category/<int:id>", CategoryDetailAPI.as_view()),
    path("/category/change-order-number", CategoryOrderChangingAPI.as_view()),
    path("/<int:id>", ToDoDetailAPI.as_view()),
    path("/change-order-number", ToDoOrderChangingAPI.as_view()),
    path("/completed", CompletedListAPI.as_view()),
    path("/completed/today", CompletedTodayListAPI.as_view()),
    path("/completed/<int:id>", CompletedDetailAPI.as_view()),
]