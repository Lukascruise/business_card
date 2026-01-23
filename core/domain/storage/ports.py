'''
from typing import Any, Protocol


class StoragePort(Protocol):
    """저장소 조작을 위한 추상 인터페이스"""

    def generate_presigned_url(self, key: str, expires_in: int = 3600) -> str: ...
    def upload_file(self, file: Any, key: str) -> str: ...
    def delete_file(self, key: str) -> None: ...
'''
