from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="home"),
    path("anime/id=<int:anime_id>", views.index_two, name="anime-view"),
]