from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),  # Halaman setelah login
    path('generateai/', views.ai_generate, name='generate_ai'),
    path('register/', views.register_view, name='register'),
    path('tryai/', views.ai_view, name='tryai'),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
]