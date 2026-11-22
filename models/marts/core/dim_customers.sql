WITH customers AS (
    SELECT * FROM {{ ref('stg_customers') }}
),

order_summary AS (
    SELECT * FROM {{ ref('int_customer_orders_summary') }}
),

final AS (
    SELECT
        c.customer_id,
        c.full_name,
        c.email,
        c.country_code,
        c.acquisition_channel,
        c.customer_status,
        c.registered_at,
        c.registered_date,
        COALESCE(s.total_orders_placed, 0) AS total_orders_placed,
        COALESCE(s.completed_orders_count, 0) AS completed_orders_count,
        COALESCE(s.lifetime_spend_usd, 0.00) AS lifetime_spend_usd,
        COALESCE(s.average_order_value_usd, 0.00) AS average_order_value_usd,
        s.first_order_date,
        s.most_recent_order_date,
        DATE_DIFF('day', s.first_order_date, s.most_recent_order_date) AS customer_relationship_days,
        ROUND((COALESCE(s.completed_orders_count, 0)::FLOAT / NULLIF(s.total_orders_placed, 0)) * 100, 2) AS order_completion_rate_pct,
        (COALESCE(s.completed_orders_count, 0) > 1) AS is_repeat_purchaser,
        -- RFM & Customer Segment Logic
        CASE
            WHEN s.lifetime_spend_usd >= 1000.00 THEN 'VIP / High Value'
            WHEN s.completed_orders_count >= 2 THEN 'Repeat Customer'
            WHEN s.completed_orders_count = 1 THEN 'Single Buyer'
            ELSE 'Prospect / No Orders'
        END AS customer_value_segment
    FROM customers c
    LEFT JOIN order_summary s ON c.customer_id = s.customer_id
)

SELECT * FROM final
