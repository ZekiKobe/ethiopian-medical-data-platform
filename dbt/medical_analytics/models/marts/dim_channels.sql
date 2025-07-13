{{
  config(
    materialized='table',
    schema='analytics'
  )
}}

WITH channel_stats AS (
    SELECT
        channel_name,
        COUNT(*) AS total_messages,
        MIN(message_date) AS first_message_date,
        MAX(message_date) AS last_message_date,
        AVG(LENGTH(message)) AS avg_message_length,
        SUM(CASE WHEN media IS NOT NULL THEN 1 ELSE 0 END) AS total_media_messages
    FROM {{ ref('stg_telegram_messages') }}
    GROUP BY 1
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['channel_name']) }} AS channel_key,
    channel_name,
    total_messages,
    first_message_date,
    last_message_date,
    avg_message_length,
    total_media_messages,
    total_media_messages::FLOAT / NULLIF(total_messages, 0) AS media_ratio
FROM channel_stats