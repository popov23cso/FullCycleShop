SELECT
    {{ list_raw_metadata() }}
    id::STRING AS ID,
    last_login::TIMESTAMP AS LAST_LOGIN,
    is_superuser::BOOLEAN AS IS_SUPERUSER,
    username::STRING AS USERNAME,
    email::STRING AS EMAIL,
    is_staff::BOOLEAN AS IS_STAFF,
    is_active::BOOLEAN AS IS_ACTIVE,
    date_joined::TIMESTAMP AS DATE_JOINED,
    first_name::STRING AS FIRST_NAME,
    last_name::STRING AS LAST_NAME,
    phone_number::STRING AS PHONE_NUMBER,
    total_purchased_amount::DECIMAL AS TOTAL_PURCHASED_AMOUNT,
    is_deleted::BOOLEAN AS IS_DELETED,
    is_api_user::BOOLEAN AS IS_API_USER,
    created_date::TIMESTAMP AS CREATED_DATE,
    updated_date::TIMESTAMP AS UPDATED_DATE,
    coalesce(generated_date, '2025-01-01T10:10:10Z')::TIMESTAMP AS GENERATED_DATETIME,
    GENERATED_DATETIME::DATE AS GENERATED_DATE
FROM {{ref('raw_djangomart_users')}}
