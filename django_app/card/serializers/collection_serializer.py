from rest_framework import serializers

from django_app.card.models.user_collection import UserCollection


class CollectionItemSerializer(serializers.Serializer):
    """보관함 목록 한 건 (수집한 명함 요약)."""

    collection_id = serializers.UUIDField(source="id")
    card_id = serializers.UUIDField(source="card.id")
    collected_at = serializers.DateTimeField()
    name = serializers.CharField(source="card.name")
    company = serializers.CharField(source="card.company", allow_null=True)
    position = serializers.CharField(source="card.position", allow_null=True)
    image_url = serializers.SerializerMethodField()

    def get_image_url(self, obj: UserCollection):
        first = obj.card.images.first()
        return first.image_url if first else None


class CollectionCreateSerializer(serializers.Serializer):
    card_id = serializers.UUIDField()


class CollectionCreateResponseSerializer(serializers.Serializer):
    collection_id = serializers.CharField()
