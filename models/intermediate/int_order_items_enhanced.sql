WITH items AS (
    SELECT * FROM {{ ref('stg_order_items') }}
),

products AS (
    SELECT * FROM {{ ref('stg_products') }}
),

joined AS (
    SELECT
        items.order_item_id,
        items.order_id,
        items.product_id,
        items.quantity,
        items.unit_sale_price_usd,
        items.line_item_amount_usd,
        products.sku,
        products.product_name,
        products.category AS product_category,
        products.unit_cost_usd,
        (products.unit_cost_usd * items.quantity)::DECIMAL(10, 2) AS line_item_cogs_usd,
        (items.line_item_amount_usd - (products.unit_cost_usd * items.quantity))::DECIMAL(10, 2) AS line_item_gross_profit_usd
    FROM items
    LEFT JOIN products ON items.product_id = products.product_id
)

SELECT * FROM joined
