{{
  config(
    materialized='table',
    schema='analytics'
  )
}}

WITH medical_classes AS (
    SELECT * FROM (VALUES
        ('pill'),
        ('medicine'),
        ('bottle'),
        ('syringe'),
        ('tablet'),
        ('cream'),
        ('vaccine')
    ) AS t(class_name)
)

SELECT
    {{ dbt_utils.generate_surrogate_key(['d.message_id', 'd.class_id', 'd.bbox']) }} AS detection_key,
    m.message_key,
    d.message_id,
    d.class_id,
    d.class_name,
    d.confidence,
    d.bbox::JSONB AS bounding_box,
    CASE WHEN mc.class_name IS NOT NULL THEN TRUE ELSE FALSE END AS is_medical
FROM {{ source('raw', 'image_detections') }} d
JOIN {{ ref('fct_messages') }} m ON d.message_id = m.message_id
LEFT JOIN medical_classes mc ON LOWER(d.class_name) = mc.class_name