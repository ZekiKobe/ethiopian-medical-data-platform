-- Custom test to ensure messages have either text or media
SELECT 
    message_key
FROM {{ ref('fct_messages') }}
WHERE (message IS NULL OR LENGTH(message) = 0)
AND has_media = FALSE