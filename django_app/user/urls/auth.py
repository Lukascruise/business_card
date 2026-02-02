from django.urls import path

from django_app.user.views.user_view import LoginView, SignupView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
    path("login", LoginView.as_view(), name="login"),
]
