
from django.urls import path
from .views import register, login_view

urlpatterns = [
    path('register/', register, name='reg'),
    path('', login_view, name='login'),
]