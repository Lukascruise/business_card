from typing import cast

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from core.constants import ApiKeys
from django_app.card.serializers.media_serializer import (
    PresignedUrlRequestSerializer,
    PresignedUrlResponseSerializer,
)
from django_app.card.services.media_service import MediaService


@extend_schema(tags=["media"])
class PresignedUrlView(APIView):
    """Cloudflare R2 직접 업로드용 주소 발급 (GET: query params, POST: body)"""

    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter("filename", str, description="파일명"),
            OpenApiParameter("file_type", str, required=False, description="MIME 타입"),
        ],
        responses={200: PresignedUrlResponseSerializer},
    )
    def get(self, request):
        serializer = PresignedUrlRequestSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, object], serializer.validated_data)
        result = MediaService.create_presigned_upload(
            filename=cast(str, data["filename"]),
            file_type=cast(str | None, data.get("file_type")),
        )
        return Response(
            {
                ApiKeys.UPLOAD_URL: result["upload_url"],
                ApiKeys.IMAGE_URL: result["image_url"],
            }
        )

    @extend_schema(
        request=PresignedUrlRequestSerializer,
        responses={200: PresignedUrlResponseSerializer},
    )
    def post(self, request):
        serializer = PresignedUrlRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = cast(dict[str, object], serializer.validated_data)
        result = MediaService.create_presigned_upload(
            filename=cast(str, data["filename"]),
            file_type=cast(str | None, data.get("file_type")),
        )
        return Response(
            {
                ApiKeys.UPLOAD_URL: result["upload_url"],
                ApiKeys.IMAGE_URL: result["image_url"],
            }
        )
