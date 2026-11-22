WITH orders AS (
    SELECT * FROM {{ ref('fct_order') }}
),

customers AS (
    SELECT * FROM {{ ref('dim_customers') }}
),

joined AS (
    SELECT
        o.order_date,
        c.acquisition_channel,
        -- Order volume metrics
        COUNT(o.order_id) AS total_orders,
        COUNT(CASE WHEN o.is_completed_order THEN o.order_id END) AS completed_orders,
        COUNT(CASE WHEN o.order_status = 'cancelled' THEN o.order_id END) AS cancelled_orders,
        ROUND(
            (COUNT(CASE WHEN o.is_completed_order THEN o.order_id END)::FLOAT / NULLIF(COUNT(o.order_id), 0)) * 100,
            2
        ) AS order_fulfillment_rate_pct,
        COUNT(DISTINCT CASE WHEN o.is_completed_order THEN o.customer_id END) AS unique_purchasing_customers,
        -- Unit and basket economics
        SUM(CASE WHEN o.is_completed_order THEN o.total_units_sold ELSE 0 END) AS total_units_sold,
        ROUND(
            SUM(CASE WHEN o.is_completed_order THEN o.total_units_sold ELSE 0 END)::FLOAT / 
            NULLIF(COUNT(CASE WHEN o.is_completed_order THEN o.order_id END), 0),
            2
        ) AS avg_units_per_order,
        -- Revenue and discounting
        SUM(CASE WHEN o.is_completed_order THEN o.subtotal_usd ELSE 0 END) AS total_subtotal_usd,
        SUM(CASE WHEN o.is_completed_order THEN o.discount_usd ELSE 0 END) AS total_discounts_usd,
        ROUND(
            (SUM(CASE WHEN o.is_completed_order THEN o.discount_usd ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN o.is_completed_order THEN o.subtotal_usd ELSE 0 END), 0)) * 100,
            2
        ) AS discount_rate_pct,
        SUM(CASE WHEN o.is_completed_order THEN o.total_amount_usd ELSE 0 END) AS gross_merchandise_value_usd,
        SUM(CASE WHEN o.order_status = 'cancelled' THEN o.total_amount_usd ELSE 0 END) AS lost_revenue_cancelled_usd,
        -- Average Order Value (AOV) & ARPU
        ROUND(
            SUM(CASE WHEN o.is_completed_order THEN o.total_amount_usd ELSE 0 END) / 
            NULLIF(COUNT(CASE WHEN o.is_completed_order THEN o.order_id END), 0),
            2
        ) AS average_order_value_usd,
        ROUND(
            SUM(CASE WHEN o.is_completed_order THEN o.total_amount_usd ELSE 0 END) / 
            NULLIF(COUNT(DISTINCT CASE WHEN o.is_completed_order THEN o.customer_id END), 0),
            2
        ) AS avg_revenue_per_purchaser_usd,
        -- Cost and profitability
        SUM(CASE WHEN o.is_completed_order THEN o.order_cogs_usd ELSE 0 END) AS total_cogs_usd,
        SUM(CASE WHEN o.is_completed_order THEN o.gross_profit_usd ELSE 0 END) AS total_gross_profit_usd,
        ROUND(
            (SUM(CASE WHEN o.is_completed_order THEN o.gross_profit_usd ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN o.is_completed_order THEN o.total_amount_usd ELSE 0 END), 0)) * 100, 2
        ) AS gross_margin_percentage,
        SUM(CASE WHEN o.is_completed_order THEN o.payment_fees_usd ELSE 0 END) AS total_payment_fees_usd,
        SUM(CASE WHEN o.is_completed_order THEN o.net_order_profit_usd ELSE 0 END) AS total_net_profit_usd,
        ROUND(
            (SUM(CASE WHEN o.is_completed_order THEN o.net_order_profit_usd ELSE 0 END) / 
            NULLIF(SUM(CASE WHEN o.is_completed_order THEN o.total_amount_usd ELSE 0 END), 0)) * 100, 2
        ) AS net_profit_margin_pct
    FROM orders o
    LEFT JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY o.order_date, c.acquisition_channel
)

SELECT * FROM joined
ORDER BY order_date DESC, gross_merchandise_value_usd DESC
