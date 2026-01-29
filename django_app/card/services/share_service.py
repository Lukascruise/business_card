from __future__ import annotations

import datetime

from django.db import transaction

from core.domain.errors import EMS, BusinessException
from django_app.card.models.card import Card
from django_app.card.models.card_event import CardEvent
from django_app.card.models.card_share import CardShareToken
from django_app.card.models.card_snapshot import CardSnapshot


class ShareService:
    @staticmethod
    def _ensure_snapshot(*, card: Card) -> CardSnapshot:
        snapshot = CardSnapshot.objects.filter(card=card).first()
        if snapshot is not None:
            return snapshot

        # 스냅샷 생성 정책(최소 필드)은 서비스 레이어 책임
        return CardSnapshot.objects.create(
            card=card,
            schema_version=1,
            data={
                "name": card.name,
                "company": card.company,
                "position": card.position,
                "email": card.email,
                "phone": card.phone,
                "bio": card.bio,
            },
        )

    @staticmethod
    @transaction.atomic
    def create_token(*, card: Card, expires_at: datetime.datetime) -> CardShareToken:
        snapshot = ShareService._ensure_snapshot(card=card)
        token = CardShareToken.objects.create(
            card=card, snapshot=snapshot, expires_at=expires_at
        )

        CardEvent.objects.create(
            card=card,
            event_type=CardEvent.EventType.SHARED,
            meta={"share_token_id": str(token.id), "snapshot_id": str(snapshot.id)},
        )

        return token

    @staticmethod
    @transaction.atomic
    def deactivate_token(*, token: CardShareToken) -> CardShareToken:
        if token.is_active:
            token.is_active = False
            token.save(update_fields=["is_active"])
        return token

    @staticmethod
    def get_snapshot_by_access_key(*, access_key: str) -> CardSnapshot:
        share = (
            CardShareToken.objects.select_related("snapshot")
            .filter(access_key=access_key)
            .first()
        )
        if (
            share is None
            or (not share.is_active)
            or share.is_expired
            or share.snapshot is None
        ):
            raise BusinessException(*EMS.AUTH_INVALID_TOKEN)
        return share.snapshot
