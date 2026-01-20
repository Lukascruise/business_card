from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from django_app.infra.r2_adapter import R2StorageAdapter


class PresignedUrlView(APIView):
    """Cloudflare R2 직접 업로드용 주소 발급"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        filename = request.data.get("filename")
        r2 = R2StorageAdapter()
        upload_url = r2.generate_presigned_url(f"temp/{filename}")
        return Response({"upload_url": upload_url})
