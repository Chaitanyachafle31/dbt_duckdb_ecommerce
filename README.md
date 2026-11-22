# Production dbt Core + DuckDB Medallion Warehouse

A complete, production-grade local modern data stack built with **dbt Core** and **DuckDB**, implementing the **Medallion Data Warehouse Architecture** (Raw &rarr; Staging &rarr; Intermediate &rarr; Marts).

---

## 1. Architecture Overview (Medallion Pattern)

```
       +-------------------------------------------------------------+
       |                         RAW LAYER                           |
       |  Raw uncleaned transactional files (seeds/*.csv)            |
       |  Tables: raw_customers, raw_orders, raw_order_items, etc.   |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |                   BRONZE / STAGING LAYER                    |
       |  models/staging/*.sql (Views)                               |
       |  - Renaming to standard snake_case                          |
       |  - Type casting & null handling                             |
       |  - Text cleaning (trim, lower, email normalization)         |
       |  - Unit conversions (cents -> dollars via Jinja macros)     |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |                   SILVER / INTERMEDIATE                     |
       |  models/intermediate/*.sql (Views)                          |
       |  - Multi-table joins & business logic                       |
       |  - Order item aggregation to order level                    |
       |  - Financial metrics (gross margin, profit, item count)     |
       |  - Customer lifetime order history summaries                |
       +------------------------------+------------------------------+
                                      |
                                      v
       +-------------------------------------------------------------+
       |                     GOLD / MARTS LAYER                      |
       |  models/marts/ (Physical Tables)                            |
       |                                                             |
       |  [Core Star Schema]                                         |
       |  - dim_customers : Customer dimension & lifetime metrics    |
       |  - dim_products  : Product catalog & margin tiers           |
       |  - fct_orders    : Transaction fact table with metrics      |
       |                                                             |
       |  [Business Reporting]                                       |
       |  - rpt_monthly_sales_metrics : Monthly revenue & AOV trends  |
       |  - rpt_customer_rfm_segments : Marketing RFM segmentation   |
       +-------------------------------------------------------------+
```

---

## 2. Directory Structure

```
dbt_duckdb_ecommerce/
├── data/
│   └── ecommerce.duckdb           # DuckDB embedded database file containing all schemas
├── dbt_project.yml                # Main dbt configuration and model materialization settings
├── profiles.yml                   # DuckDB connection profile
├── macros/
│   ├── cents_to_dollars.sql       # Jinja macro converting currency from cents to dollars
│   └── generate_schema_name.sql   # Custom macro for clean schema naming in DuckDB
├── models/
│   ├── staging/                   # Bronze Layer (Views)
│   │   ├── _staging__sources.yml  # Source declarations & raw data tests
│   │   ├── _staging__models.yml   # Staging model definitions & column tests
│   │   ├── stg_ecommerce__customers.sql
│   │   ├── stg_ecommerce__order_items.sql
│   │   ├── stg_ecommerce__orders.sql
│   │   └── stg_ecommerce__products.sql
│   ├── intermediate/              # Silver Layer (Views)
│   │   ├── _intermediate__models.yml
│   │   ├── int_customer_orders_summary.sql
│   │   ├── int_order_items_summary.sql
│   │   └── int_orders_enriched.sql
│   └── marts/                     # Gold Layer (Tables)
│       ├── core/
│       │   ├── _core__models.yml
│       │   ├── dim_customers.sql
│       │   ├── dim_products.sql
│       │   └── fct_orders.sql
│       └── reporting/
│           ├── _reporting__models.yml
│           ├── rpt_customer_rfm_segments.sql
│           └── rpt_monthly_sales_metrics.sql
├── seeds/                         # Raw transactional data (CSV)
│   ├── raw_customers.csv
│   ├── raw_order_items.csv
│   ├── raw_orders.csv
│   └── raw_products.csv
└── tests/                         # Custom Singular Tests
    └── assert_order_total_is_positive.sql
```

---

## 3. How to Run This Project in the IDE

Open a terminal in your IDE at `d:\AntigravityIDE\dbt_duckdb_ecommerce`.

### Step 1: Ensure Environment Variables & Dependencies
```powershell
$env:USERPROFILE = "d:\AntigravityIDE"
$env:HOME = "d:\AntigravityIDE"
```

### Step 2: Test the DuckDB Connection
Verify that dbt can read your `profiles.yml` and connect to DuckDB:
```powershell
..\.venv\Scripts\dbt.exe debug --profiles-dir .
```

### Step 3: Seed Raw Data into DuckDB
Loads all CSVs in `seeds/` into the `raw` schema inside `data/ecommerce.duckdb`:
```powershell
..\.venv\Scripts\dbt.exe seed --profiles-dir .
```

### Step 4: Run Transformations
Executes all SQL models across Staging, Intermediate, and Marts:
```powershell
..\.venv\Scripts\dbt.exe run --profiles-dir .
```

### Step 5: Run Automated Data Tests
Executes all 40 schema constraints (`unique`, `not_null`, `accepted_values`, `relationships`) and singular assertions:
```powershell
..\.venv\Scripts\dbt.exe test --profiles-dir .
```

### Step 6: Generate and Serve Documentation Lineage Graph
```powershell
..\.venv\Scripts\dbt.exe docs generate --profiles-dir .
```

---

## 4. Querying the DuckDB Database Directly

You can query your warehouse directly in Python:

```python
import duckdb

conn = duckdb.connect('data/ecommerce.duckdb')

# Inspect monthly sales metrics
conn.sql('SELECT * FROM marts.rpt_monthly_sales_metrics').show()

# Inspect customer segmentation
conn.sql('SELECT full_name, customer_segment, monetary, recency_days FROM marts.rpt_customer_rfm_segments').show()
```
