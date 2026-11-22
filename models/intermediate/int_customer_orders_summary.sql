WITH orders AS (
    SELECT * FROM {{ ref('stg_orders') }}
),

aggregated AS (
    SELECT
        customer_id,
        MIN(order_date) AS first_order_date,
        MAX(order_date) AS most_recent_order_date,
        COUNT(order_id) AS total_orders_placed,
        COUNT(CASE WHEN is_completed_order THEN order_id END) AS completed_orders_count,
        COALESCE(SUM(CASE WHEN is_completed_order THEN total_amount_usd ELSE 0 END), 0)::DECIMAL(10, 2) AS lifetime_spend_usd,
        ROUND(AVG(CASE WHEN is_completed_order THEN total_amount_usd END), 2)::DECIMAL(10, 2) AS average_order_value_usd
    FROM orders
    GROUP BY customer_id
)

SELECT * FROM aggregated
