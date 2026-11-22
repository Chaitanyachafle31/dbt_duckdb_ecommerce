from pathlib import Path
import duckdb

DB_PATH = Path(__file__).resolve().parent.parent / "dev.duckdb"


def init_duckdb():
    print(f"🔌 Connecting to {DB_PATH.name}...")
    con = duckdb.connect(str(DB_PATH))

    # 1. Create Schema
    con.sql("CREATE SCHEMA IF NOT EXISTS raw")
    print("✅ Created schema 'raw'")

    # 2. Customers Table
    con.sql("""
    CREATE TABLE IF NOT EXISTS raw.raw_customers (
        customer_id VARCHAR,
        first_name VARCHAR,
        last_name VARCHAR,
        email VARCHAR,
        country_code VARCHAR,
        acquisition_channel VARCHAR,
        created_at TIMESTAMP,
        status VARCHAR
    );
    """)

    con.sql("""
    INSERT INTO raw.raw_customers (customer_id, first_name, last_name, email, country_code, acquisition_channel, created_at, status) VALUES
        ('cust_101', 'Elena', 'Rostova', 'elena.rostova@datadrive.io', 'US', 'organic_search', '2026-01-15 08:24:12', 'active'),
        ('cust_102', 'Marcus', 'Chen', 'marcus.chen@finscale.co', 'US', 'linkedin_ads', '2026-01-18 14:11:05', 'active'),
        ('cust_103', 'Sophia', 'Alvarez', 'sophia.alvarez@cloudpeak.es', 'ES', 'referral', '2026-02-02 11:45:30', 'active'),
        ('cust_104', 'Liam', 'O''Connor', 'liam.oconnor@dublinanalytics.ie', 'IE', 'podcast', '2026-02-10 16:30:19', 'active'),
        ('cust_105', 'Aisha', 'Patel', 'aisha.patel@mumbaitech.in', 'IN', 'organic_search', '2026-02-22 09:15:44', 'active'),
        ('cust_106', 'David', 'Mueller', 'david.mueller@berlindata.de', 'DE', 'newsletter', '2026-03-05 13:50:22', 'active'),
        ('cust_107', 'Chloe', 'Dubois', 'chloe.dubois@parislakehouse.fr', 'FR', 'webinar', '2026-03-14 10:02:18', 'active'),
        ('cust_108', 'Tariq', 'Al-Mansoor', 'tariq.mansoor@gulfcloud.ae', 'AE', 'direct_sales', '2026-03-25 17:40:00', 'active'),
        ('cust_109', 'Kavita', 'Reddy', 'kavita.reddy@bengaluruai.in', 'IN', 'referral', '2026-04-01 07:22:15', 'active'),
        ('cust_110', 'Lucas', 'Silva', 'lucas.silva@saopaulometrix.br', 'BR', 'organic_search', '2026-04-12 12:18:33', 'churned'),
        ('cust_111', 'Zoe', 'Tremblay', 'zoe.tremblay@montrealbi.ca', 'CA', 'linkedin_ads', '2026-04-20 15:33:51', 'active'),
        ('cust_112', 'Kenji', 'Takahashi', 'kenji.takahashi@tokyopipelines.jp', 'JP', 'webinar', '2026-05-04 09:44:12', 'active'),
        ('cust_113', 'Hannah', 'Schmidt', 'hannah.schmidt@munichdw.de', 'DE', 'podcast', '2026-05-18 18:20:00', 'active'),
        ('cust_114', 'Arthur', 'Pendelton', 'arthur.p@londonfinops.uk', 'GB', 'direct_sales', '2026-06-01 11:10:45', 'active'),
        ('cust_115', 'Fatima', 'Bello', 'fatima.bello@lagoscompute.ng', 'NG', 'organic_search', '2026-06-15 14:05:30', 'active');
    """)
    print("✅ Initialized raw.raw_customers")

    # 3. Products Table
    con.sql("""
    CREATE TABLE IF NOT EXISTS raw.raw_products (
        product_id VARCHAR,
        sku VARCHAR,
        product_name VARCHAR,
        category VARCHAR,
        unit_cost_cents INTEGER,
        retail_price_cents INTEGER,
        is_active BOOLEAN
    );
    """)

    con.sql("""
    INSERT INTO raw.raw_products (product_id, sku, product_name, category, unit_cost_cents, retail_price_cents, is_active) VALUES
        ('prod_001', 'DD-ENG-PRO', 'Data Solutions Architect License (Annual)', 'Software & Learning', 8000, 29900, TRUE),
        ('prod_002', 'DD-ENG-EXEC', 'Enterprise Architecture Advisory Pass', 'Consulting', 35000, 95000, TRUE),
        ('prod_003', 'DD-SIM-TEAM', 'Multi-User Pipeline Simulator (10 Seats)', 'SaaS Tools', 12000, 49000, TRUE),
        ('prod_004', 'DD-CLD-AUDIT', 'Snowflake & FinOps Cost Audit Pack', 'Audit Tools', 5000, 19900, TRUE),
        ('prod_005', 'DD-DBT-WKSHP', 'Production dbt Core Masterclass Voucher', 'Workshops', 4000, 14900, TRUE),
        ('prod_006', 'DD-INT-KIT', 'Data Architect Interview Decoders Book', 'Publications', 1500, 4900, TRUE),
        ('prod_007', 'DD-AI-GOV', 'Enterprise AI Governance Blueprint', 'Publications', 2000, 7900, TRUE),
        ('prod_008', 'DD-FABRIC-ACC', 'Microsoft Fabric Migration Accelerator', 'Software & Learning', 15000, 59900, FALSE);
    """)
    print("✅ Initialized raw.raw_products")

    # 4. Orders Table
    con.sql("""
    CREATE TABLE IF NOT EXISTS raw.raw_orders (
        order_id VARCHAR,
        customer_id VARCHAR,
        order_status VARCHAR,
        order_date DATE,
        currency VARCHAR,
        subtotal_cents INTEGER,
        tax_cents INTEGER,
        shipping_cents INTEGER,
        discount_cents INTEGER,
        total_amount_cents INTEGER
    );
    """)

    con.sql("""
    INSERT INTO raw.raw_orders (order_id, customer_id, order_status, order_date, currency, subtotal_cents, tax_cents, shipping_cents, discount_cents, total_amount_cents) VALUES
        ('ord_1001', 'cust_101', 'completed', '2026-01-20', 'USD', 29900, 2392, 0, 2990, 29302),
        ('ord_1002', 'cust_102', 'completed', '2026-01-25', 'USD', 95000, 7600, 0, 0, 102600),
        ('ord_1003', 'cust_103', 'completed', '2026-02-05', 'EUR', 49000, 10290, 0, 4900, 54390),
        ('ord_1004', 'cust_104', 'completed', '2026-02-14', 'EUR', 19900, 4577, 0, 0, 24477),
        ('ord_1005', 'cust_105', 'completed', '2026-03-01', 'USD', 29900, 5382, 0, 5000, 30282),
        ('ord_1006', 'cust_101', 'completed', '2026-03-10', 'USD', 14900, 1192, 0, 1490, 14602),
        ('ord_1007', 'cust_106', 'completed', '2026-03-18', 'EUR', 49000, 9310, 0, 0, 58310),
        ('ord_1008', 'cust_107', 'cancelled', '2026-03-22', 'EUR', 29900, 5980, 0, 2990, 32890),
        ('ord_1009', 'cust_108', 'completed', '2026-03-29', 'USD', 95000, 4750, 0, 9500, 90250),
        ('ord_1010', 'cust_109', 'completed', '2026-04-05', 'USD', 29900, 5382, 0, 0, 35282),
        ('ord_1011', 'cust_102', 'completed', '2026-04-15', 'USD', 49000, 3920, 0, 4900, 48020),
        ('ord_1012', 'cust_110', 'returned', '2026-04-18', 'USD', 19900, 1592, 0, 0, 21492),
        ('ord_1013', 'cust_111', 'completed', '2026-04-28', 'CAD', 29900, 3887, 0, 2990, 30797),
        ('ord_1014', 'cust_112', 'completed', '2026-05-10', 'USD', 14900, 1490, 0, 0, 16390),
        ('ord_1015', 'cust_113', 'completed', '2026-05-22', 'EUR', 95000, 18050, 0, 9500, 103550),
        ('ord_1016', 'cust_114', 'completed', '2026-06-05', 'GBP', 49000, 9800, 0, 0, 58800),
        ('ord_1017', 'cust_115', 'completed', '2026-06-20', 'USD', 29900, 2242, 0, 2990, 29152),
        ('ord_1018', 'cust_105', 'completed', '2026-07-02', 'USD', 14900, 2682, 0, 0, 17582),
        ('ord_1019', 'cust_101', 'completed', '2026-07-15', 'USD', 4900, 392, 0, 0, 5292),
        ('ord_1020', 'cust_103', 'pending', '2026-07-28', 'EUR', 29900, 6279, 0, 2990, 33189);
    """)
    print("✅ Initialized raw.raw_orders")

    # 5. Order Items Table
    con.sql("""
    CREATE TABLE IF NOT EXISTS raw.raw_order_items (
        order_item_id VARCHAR,
        order_id VARCHAR,
        product_id VARCHAR,
        quantity INTEGER,
        unit_sale_price_cents INTEGER,
        total_item_cents INTEGER
    );
    """)

    con.sql("""
    INSERT INTO raw.raw_order_items (order_item_id, order_id, product_id, quantity, unit_sale_price_cents, total_item_cents) VALUES
        ('item_01', 'ord_1001', 'prod_001', 1, 29900, 29900),
        ('item_02', 'ord_1002', 'prod_002', 1, 95000, 95000),
        ('item_03', 'ord_1003', 'prod_003', 1, 49000, 49000),
        ('item_04', 'ord_1004', 'prod_004', 1, 19900, 19900),
        ('item_05', 'ord_1005', 'prod_001', 1, 29900, 29900),
        ('item_06', 'ord_1006', 'prod_005', 1, 14900, 14900),
        ('item_07', 'ord_1007', 'prod_003', 1, 49000, 49000),
        ('item_08', 'ord_1008', 'prod_001', 1, 29900, 29900),
        ('item_09', 'ord_1009', 'prod_002', 1, 95000, 95000),
        ('item_10', 'ord_1010', 'prod_001', 1, 29900, 29900),
        ('item_11', 'ord_1011', 'prod_003', 1, 49000, 49000),
        ('item_12', 'ord_1012', 'prod_004', 1, 19900, 19900),
        ('item_13', 'ord_1013', 'prod_001', 1, 29900, 29900),
        ('item_14', 'ord_1014', 'prod_005', 1, 14900, 14900),
        ('item_15', 'ord_1015', 'prod_002', 1, 95000, 95000),
        ('item_16', 'ord_1016', 'prod_003', 1, 49000, 49000),
        ('item_17', 'ord_1017', 'prod_001', 1, 29900, 29900),
        ('item_18', 'ord_1018', 'prod_005', 1, 14900, 14900),
        ('item_19', 'ord_1019', 'prod_006', 1, 4900, 4900),
        ('item_20', 'ord_1020', 'prod_001', 1, 29900, 29900);
    """)
    print("✅ Initialized raw.raw_order_items")

    # 6. Payments Table
    con.sql("""
    CREATE TABLE IF NOT EXISTS raw.raw_payments (
        payment_id VARCHAR,
        order_id VARCHAR,
        payment_method VARCHAR,
        gateway VARCHAR,
        payment_status VARCHAR,
        amount_cents INTEGER,
        fee_cents INTEGER,
        processed_at TIMESTAMP
    );
    """)

    con.sql("""
    INSERT INTO raw.raw_payments (payment_id, order_id, payment_method, gateway, payment_status, amount_cents, fee_cents, processed_at) VALUES
        ('pay_5001', 'ord_1001', 'credit_card', 'stripe', 'success', 29302, 879, '2026-01-20 08:26:01'),
        ('pay_5002', 'ord_1002', 'bank_transfer', 'adyen', 'success', 102600, 1539, '2026-01-25 14:15:22'),
        ('pay_5003', 'ord_1003', 'credit_card', 'stripe', 'success', 54390, 1631, '2026-02-05 11:47:10'),
        ('pay_5004', 'ord_1004', 'paypal', 'paypal', 'success', 24477, 856, '2026-02-14 16:32:00'),
        ('pay_5005', 'ord_1005', 'credit_card', 'stripe', 'success', 30282, 908, '2026-03-01 09:18:40'),
        ('pay_5006', 'ord_1006', 'credit_card', 'stripe', 'success', 14602, 438, '2026-03-10 13:52:15'),
        ('pay_5007', 'ord_1007', 'bank_transfer', 'adyen', 'success', 58310, 874, '2026-03-18 10:05:00'),
        ('pay_5008', 'ord_1008', 'credit_card', 'stripe', 'failed', 32890, 0, '2026-03-22 17:42:11'),
        ('pay_5009', 'ord_1009', 'bank_transfer', 'adyen', 'success', 90250, 1353, '2026-03-29 07:25:00'),
        ('pay_5010', 'ord_1010', 'credit_card', 'stripe', 'success', 35282, 1058, '2026-04-05 12:20:19'),
        ('pay_5011', 'ord_1011', 'credit_card', 'stripe', 'success', 48020, 1440, '2026-04-15 15:35:10'),
        ('pay_5012', 'ord_1012', 'credit_card', 'stripe', 'refunded', 21492, 644, '2026-04-18 09:46:00'),
        ('pay_5013', 'ord_1013', 'credit_card', 'stripe', 'success', 30797, 923, '2026-04-28 18:22:15'),
        ('pay_5014', 'ord_1014', 'paypal', 'paypal', 'success', 16390, 573, '2026-05-10 11:12:00'),
        ('pay_5015', 'ord_1015', 'bank_transfer', 'adyen', 'success', 103550, 1553, '2026-05-22 14:08:20'),
        ('pay_5016', 'ord_1016', 'credit_card', 'stripe', 'success', 58800, 1764, '2026-06-05 09:20:10'),
        ('pay_5017', 'ord_1017', 'credit_card', 'stripe', 'success', 29152, 874, '2026-06-20 13:55:00'),
        ('pay_5018', 'ord_1018', 'credit_card', 'stripe', 'success', 17582, 527, '2026-07-02 10:04:15'),
        ('pay_5019', 'ord_1019', 'credit_card', 'stripe', 'success', 5292, 158, '2026-07-15 17:42:30'),
        ('pay_5020', 'ord_1020', 'credit_card', 'stripe', 'pending', 33189, 0, '2026-07-28 08:30:00');
    """)
    print("✅ Initialized raw.raw_payments")

    return con


if __name__ == "__main__":
    con = init_duckdb()

    print("\n📊 Verifying table counts:")
    con.sql("""
    SELECT 'raw_customers' AS table_name, COUNT(*) AS total_rows FROM raw.raw_customers
    UNION ALL
    SELECT 'raw_products', COUNT(*) FROM raw.raw_products
    UNION ALL
    SELECT 'raw_orders', COUNT(*) FROM raw.raw_orders
    UNION ALL
    SELECT 'raw_order_items', COUNT(*) FROM raw.raw_order_items
    UNION ALL
    SELECT 'raw_payments', COUNT(*) FROM raw.raw_payments;
    """).show()
