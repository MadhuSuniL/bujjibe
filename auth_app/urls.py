from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path('login', LoginView.as_view(), name = 'Login'),
    path('register', RegisterView.as_view(), name = 'Register'),
]
