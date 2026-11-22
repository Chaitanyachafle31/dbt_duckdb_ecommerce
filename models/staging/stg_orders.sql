WITH source AS (
    SELECT DISTINCT * FROM {{ source('raw', 'raw_orders') }}

),

transformed AS (
    SELECT
        order_id,
        customer_id,
        LOWER(order_status) AS order_status,
        order_date,
        currency,
        (subtotal_cents / 100.0)::DECIMAL(10, 2) AS subtotal_usd,
        (tax_cents / 100.0)::DECIMAL(10, 2) AS tax_usd,
        (shipping_cents / 100.0)::DECIMAL(10, 2) AS shipping_usd,
        (discount_cents / 100.0)::DECIMAL(10, 2) AS discount_usd,
        (total_amount_cents / 100.0)::DECIMAL(10, 2) AS total_amount_usd,
        CASE WHEN order_status = 'completed' THEN TRUE ELSE FALSE END AS is_completed_order,
        CASE WHEN order_status = 'returned' THEN TRUE ELSE FALSE END AS is_returned_order,
        CASE WHEN order_status = 'cancelled' THEN TRUE ELSE FALSE END AS is_cancelled_order
    FROM source
)

SELECT * FROM transformed
