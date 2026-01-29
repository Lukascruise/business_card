from django.urls import include, path

urlpatterns = [
    path("auth/", include("django_app.user.urls.auth")),
    path("user/", include("django_app.user.urls.user")),
    path("", include("django_app.card.urls.v1")),
]
