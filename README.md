https://businesscardfrontend-flame.vercel.app

https://business-card-frontend-omega.vercel.app

[Request Flow]
URL
 → View
   → Permission
   → Serializer (input)
   → Service
     → Model
     → Utils
   → Serializer (output)
 → Response

현재 MVP 단계에서는 단일 스토리지(R2)만 사용하므로
Storage Port / Adapter 패턴을 의도적으로 제거

다음 조건 중 하나라도 충족되면 Port를 도입
- S3 + R2 병행
- Local storage fallback
- Storage 단위 테스트 필요

erDiagram
    USER {
        uuid id PK
        string email
        datetime created_at
    }

    USER_AUTH {
        uuid id PK
        uuid user_id FK
        string password_hash
        string auth_provider
        datetime created_at
    }

    BUSINESS_CARD {
        uuid id PK
        uuid owner_id FK
        string name
        string company
        string position
        string email
        string phone
        text bio
        datetime created_at
        datetime updated_at
    }

    USER_COLLECTION {
        uuid id PK
        uuid user_id FK
        uuid card_id FK
        datetime collected_at
    }

    CARD_IMAGE {
        uuid id PK
        uuid card_id FK
        string image_url
        text ocr_text
        float ocr_confidence
        datetime created_at
    }

    SHARE_TOKEN {
        uuid id PK
        uuid card_id FK
        uuid created_by FK
        string token
        datetime expires_at
        boolean is_active
        datetime created_at
    }

    CARD_EVENT {
        uuid id PK
        uuid card_id FK
        string event_type
        jsonb snapshot
        datetime created_at
    }

    %% Relationships
    USER ||--|| USER_AUTH : authenticates
    USER ||--o{ BUSINESS_CARD : owns
    USER ||--o{ USER_COLLECTION : collects
    USER ||--o{ SHARE_TOKEN : creates

    BUSINESS_CARD ||--o{ USER_COLLECTION : collected_as
    BUSINESS_CARD ||--o{ CARD_IMAGE : has
    BUSINESS_CARD ||--o{ SHARE_TOKEN : shared_by
    BUSINESS_CARD ||--o{ CARD_EVENT : emits
