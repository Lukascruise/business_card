from django.apps import AppConfig


class CardConfig(AppConfig):
    # 앱의 물리적 경로와 이름 정의
    default_auto_field = "django.db.models.BigAutoField"
    name = "django_app.card"
    verbose_name = "명함 관리 시스템"

    def ready(self):
        """
        앱이 준비되었을 때 실행되는 시동 로직.
        주로 시그널 등록을 여기서 수행합니다.
        """
        try:
            # 향후 시그널이 필요할 경우 여기서 임포트하여 등록
            # import django_app.card.signals
            pass
        except ImportError:
            pass
