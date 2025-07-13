{{
  config(
    materialized='view',
    schema='staging'
  )
}}

SELECT
    message_id,
    channel_name,
    date AS image_date,
    file_path,
    scraped_at
FROM {{ source('raw', 'telegram_images') }}

-- Add tests in schema.yml