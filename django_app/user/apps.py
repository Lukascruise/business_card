from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_app.user"
    verbose_name = "사용자"
    label = "user"
