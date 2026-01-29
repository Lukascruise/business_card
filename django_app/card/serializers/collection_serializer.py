from rest_framework import serializers


class CollectionCreateSerializer(serializers.Serializer):
    card_id = serializers.UUIDField()


class CollectionCreateResponseSerializer(serializers.Serializer):
    collection_id = serializers.CharField()
