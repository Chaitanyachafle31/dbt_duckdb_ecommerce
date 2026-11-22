WITH source AS (
    SELECT DISTINCT * FROM {{ source('raw', 'raw_payments') }}
),

transformed AS (
    SELECT
        payment_id,
        order_id,
        LOWER(payment_method) AS payment_method,
        LOWER(gateway) AS gateway,
        LOWER(payment_status) AS payment_status,
        (amount_cents / 100.0)::DECIMAL(10, 2) AS payment_amount_usd,
        (fee_cents / 100.0)::DECIMAL(10, 2) AS processing_fee_usd,
        ((amount_cents - fee_cents) / 100.0)::DECIMAL(10, 2) AS net_settled_amount_usd,
        processed_at,
        CASE WHEN payment_status = 'success' THEN TRUE ELSE FALSE END AS is_successful_payment
    FROM source
)

SELECT * FROM transformed
