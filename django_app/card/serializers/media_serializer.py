from rest_framework import serializers


class PresignedUrlRequestSerializer(serializers.Serializer):
    filename = serializers.CharField()
    file_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class PresignedUrlResponseSerializer(serializers.Serializer):
    upload_url = serializers.URLField()
    image_url = serializers.URLField()
