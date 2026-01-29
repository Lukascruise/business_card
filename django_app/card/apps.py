from django.apps import AppConfig


class CardConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_app.card"
    verbose_name = "명함"

    def ready(self):
        # MVP에서는 시그널을 강제하지 않음(서비스 레이어에서 동기 저장)
        # 필요 시 여기서 signals import
        return
