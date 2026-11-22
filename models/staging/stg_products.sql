WITH source AS (
    SELECT DISTINCT * FROM {{ source('raw', 'raw_products') }}
),
transformed AS (
    SELECT
        product_id,
        sku,
        product_name,
        category,
        (unit_cost_cents / 100.0)::DECIMAL(10, 2) AS unit_cost_usd,
        (retail_price_cents / 100.0)::DECIMAL(10, 2) AS retail_price_usd,
        ((retail_price_cents - unit_cost_cents) / 100.0)::DECIMAL(10, 2) AS unit_margin_usd,
        ROUND(((retail_price_cents - unit_cost_cents)::FLOAT / NULLIF(retail_price_cents, 0)) * 100, 2) AS margin_percentage,
        is_active
    FROM source
)

SELECT * FROM transformed
