WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

order_items AS (
    SELECT
        order_id,
        COUNT(order_item_id) AS items_count,
        SUM(quantity) AS total_units_sold,
        SUM(line_item_cogs_usd) AS total_order_cogs_usd,
        SUM(line_item_gross_profit_usd) AS total_order_gross_profit_usd
    FROM {{ ref('int_order_items_enhanced') }}
    GROUP BY order_id
),

payments AS (
    SELECT
        order_id,
        COUNT(payment_id) AS payments_count,
        COALESCE(SUM(CASE WHEN is_successful_payment THEN payment_amount_usd ELSE 0 END), 0) AS total_paid_amount_usd,
        COALESCE(SUM(CASE WHEN is_successful_payment THEN processing_fee_usd ELSE 0 END), 0) AS total_processing_fees_usd
    FROM {{ ref('stg_payments') }}
    GROUP BY order_id
),

final AS (
    SELECT
        o.order_id,
        o.customer_id,
        o.order_status,
        o.order_date,
        o.currency,
        o.subtotal_usd,
        o.discount_usd,
        o.tax_usd,
        o.shipping_usd,
        o.total_amount_usd,
        COALESCE(i.items_count, 0) AS items_count,
        COALESCE(i.total_units_sold, 0) AS total_units_sold,
        COALESCE(i.total_order_cogs_usd, 0.00) AS order_cogs_usd,
        COALESCE(i.total_order_gross_profit_usd, 0.00) AS gross_profit_usd,
        ROUND((COALESCE(i.total_order_gross_profit_usd, 0) / NULLIF(o.total_amount_usd, 0)) * 100, 2) AS gross_margin_pct,
        COALESCE(p.total_paid_amount_usd, 0.00) AS total_paid_amount_usd,
        COALESCE(p.total_processing_fees_usd, 0.00) AS payment_fees_usd,
        (COALESCE(p.total_paid_amount_usd, 0) - COALESCE(p.total_processing_fees_usd, 0))::DECIMAL(10, 2) AS net_settled_revenue_usd,
        (COALESCE(i.total_order_gross_profit_usd, 0.00) - COALESCE(p.total_processing_fees_usd, 0.00))::DECIMAL(10, 2) AS net_order_profit_usd,
        ROUND(
            ((COALESCE(i.total_order_gross_profit_usd, 0) - COALESCE(p.total_processing_fees_usd, 0)) / NULLIF(o.total_amount_usd, 0)) * 100,
            2
        ) AS net_order_margin_pct,
        ROUND((o.discount_usd / NULLIF(o.subtotal_usd, 0)) * 100, 2) AS discount_pct,
        ROUND(o.subtotal_usd / NULLIF(COALESCE(i.total_units_sold, 0), 0), 2) AS avg_item_unit_price_usd,
        o.is_completed_order
    FROM orders o
    LEFT JOIN order_items i ON o.order_id = i.order_id
    LEFT JOIN payments p ON o.order_id = p.order_id
)

SELECT * FROM final
