WITH source AS (
    SELECT DISTINCT * FROM {{ source('raw', 'raw_order_items') }}
  
),

transformed AS (
    SELECT
        order_item_id,
        order_id,
        product_id,
        quantity,
        (unit_sale_price_cents / 100.0)::DECIMAL(10, 2) AS unit_sale_price_usd,
        (total_item_cents / 100.0)::DECIMAL(10, 2) AS line_item_amount_usd
    FROM source
)
SELECT * FROM transformed
