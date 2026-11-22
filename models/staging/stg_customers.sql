WITH source AS (
    SELECT DISTINCT * FROM {{ source('raw', 'raw_customers') }}
),

renamed AS (
    SELECT
        customer_id,
        TRIM(first_name) AS first_name,
        TRIM(last_name) AS last_name,
        CONCAT(TRIM(first_name), ' ', TRIM(last_name)) AS full_name,
        LOWER(TRIM(email)) AS email,
        UPPER(country_code) AS country_code,
        LOWER(acquisition_channel) AS acquisition_channel,
        status AS customer_status,
        created_at AS registered_at,
        created_at::DATE AS registered_date
    FROM source
)

SELECT * FROM renamed