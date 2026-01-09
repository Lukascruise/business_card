```mermaid
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
    ```
