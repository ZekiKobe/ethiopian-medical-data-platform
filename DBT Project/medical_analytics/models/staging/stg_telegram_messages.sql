{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT
    id AS message_id,
    date AS message_date,
    message,
    views,
    media,
    channel AS channel_name,
    scraped_at
FROM {{ source('raw', 'telegram_messages') }}

-- Add tests in schema.yml