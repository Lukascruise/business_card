from django.urls import path

from django_app.user.views.user_view import SignupView

urlpatterns = [
    path("signup", SignupView.as_view(), name="signup"),
]
