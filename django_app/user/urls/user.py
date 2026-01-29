from django.urls import path

from django_app.user.views.user_view import UserProfileView

urlpatterns = [
    path("profile", UserProfileView.as_view(), name="user-profile"),
]
