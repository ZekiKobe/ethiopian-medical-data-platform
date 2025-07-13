{{
  config(
    materialized='table',
    schema='analytics'
  )
}}

WITH messages_with_products AS (
    SELECT
        m.message_id,
        m.channel_name,
        m.message_date,
        m.message,
        m.views,
        m.media,
        m.scraped_at,
        -- Extract potential product mentions (simple regex for demo)
        REGEXP_MATCHES(LOWER(m.message), '(paracetamol|amoxicillin|insulin|vaccine|antibiotic|cream|pills?|tablets?)', 'g') AS product_mentions
    FROM {{ ref('stg_telegram_messages') }} m
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['message_id', 'channel_name']) }} AS message_key,
    d.channel_key,
    dd.date_key,
    m.message_id,
    m.channel_name,
    m.message_date,
    m.message,
    m.views,
    m.media,
    LENGTH(m.message) AS message_length,
    CASE WHEN m.media IS NOT NULL THEN TRUE ELSE FALSE END AS has_media,
    ARRAY_LENGTH(m.product_mentions, 1) AS product_mention_count,
    m.scraped_at
FROM messages_with_products m
JOIN {{ ref('dim_channels') }} d ON m.channel_name = d.channel_name
JOIN {{ ref('dim_dates') }} dd ON m.message_date::DATE = dd.date