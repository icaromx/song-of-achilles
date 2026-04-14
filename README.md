# E-Commerce Revenue Analytics Pipeline

An end-to-end data pipeline built on the [Olist Brazilian E-Commerce dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) (~100k orders, 8 relational tables). The project covers ingestion, schema design, star-schema transformation, and analytical SQL queries that answer real business questions.

**Stack:** Python · PostgreSQL · SQL (CTEs, window functions, aggregations)

---

## Business Questions Answered

| # | Question | SQL file |
|---|----------|----------|
| 1 | How does monthly revenue trend, and what drives seasonality? | `analysis/01_revenue_trends.sql` |
| 2 | What is the 30/60/90-day retention rate by customer cohort? | `analysis/02_cohort_retention.sql` |
| 3 | Which sellers rank highest on revenue, volume, and review score? | `analysis/03_seller_performance.sql` |
| 4 | Which product categories and regions have the worst late-delivery rates? | `analysis/04_delivery_analysis.sql` |

---

## Project Structure

```
ecommerce-analytics/
├── data/
│   ├── raw/                  # Downloaded Olist CSVs (git-ignored)
│   └── processed/            # Intermediate cleaned files
├── ingestion/
│   ├── load_data.py          # Loads CSVs → PostgreSQL staging tables
│   └── requirements.txt
├── sql/
│   ├── schema/
│   │   ├── 01_create_tables.sql   # Staging + star schema DDL
│   │   └── 02_indexes.sql         # Performance indexes
│   ├── transform/
│   │   ├── 01_star_schema.sql     # fact_orders, dim_customers, etc.
│   │   ├── 02_rfm_segmentation.sql
│   │   └── 03_cohort_prep.sql
│   └── analysis/
│       ├── 01_revenue_trends.sql
│       ├── 02_cohort_retention.sql
│       ├── 03_seller_performance.sql
│       └── 04_delivery_analysis.sql
├── notebooks/
│   └── eda.ipynb             # Exploratory analysis + charts
├── docs/
│   └── erd.png               # Entity-relationship diagram
├── docker-compose.yml        # Spins up a local Postgres instance
├── .env.example
└── README.md
```

---

## Quickstart

### 1. Clone and configure

```bash
git clone https://github.com/<your-username>/ecommerce-analytics.git
cd ecommerce-analytics
cp .env.example .env
# Edit .env with your Postgres credentials
```

### 2. Start Postgres (Docker)

```bash
docker-compose up -d
```

### 3. Download the dataset

Download the Olist dataset from [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce) and place the CSV files in `data/raw/`.

### 4. Install Python dependencies and load data

```bash
pip install -r ingestion/requirements.txt
python ingestion/load_data.py
```

### 5. Run the SQL pipeline in order

```bash
# Schema
psql $DATABASE_URL -f sql/schema/01_create_tables.sql
psql $DATABASE_URL -f sql/schema/02_indexes.sql

# Transform
psql $DATABASE_URL -f sql/transform/01_star_schema.sql
psql $DATABASE_URL -f sql/transform/02_rfm_segmentation.sql
psql $DATABASE_URL -f sql/transform/03_cohort_prep.sql

# Analyze
psql $DATABASE_URL -f sql/analysis/01_revenue_trends.sql
psql $DATABASE_URL -f sql/analysis/02_cohort_retention.sql
psql $DATABASE_URL -f sql/analysis/03_seller_performance.sql
psql $DATABASE_URL -f sql/analysis/04_delivery_analysis.sql
```

---

## Schema Design

The raw Olist tables are normalized into a star schema optimized for analytical queries:

```
fact_orders
├── order_id (PK)
├── customer_key (FK → dim_customers)
├── seller_key  (FK → dim_sellers)
├── product_key (FK → dim_products)
├── date_key    (FK → dim_date)
├── price
├── freight_value
├── payment_value
└── delivery_delay_days

dim_customers   dim_sellers   dim_products   dim_date
```

See `docs/erd.png` for the full entity-relationship diagram.

---

## Key SQL Techniques Demonstrated

- **Window functions** — rolling revenue (`SUM() OVER`), seller ranking (`DENSE_RANK()`), cohort indexing
- **CTEs** — multi-step transformations written as readable, modular query chains
- **Date arithmetic** — cohort assignment, delivery delay calculation, period-over-period comparisons
- **RFM segmentation** — customers scored and bucketed on Recency, Frequency, and Monetary value
- **Aggregations & filters** — category-level late delivery rates, regional breakdowns

---

## Sample Finding

> Customers acquired in **November–December** (holiday cohort) show a **42% higher 90-day return rate** than off-peak cohorts, but also account for **67% of late deliveries** due to logistics strain — a classic growth-vs-ops tradeoff.

*(Figures are illustrative; replace with your actual findings after running the pipeline.)*

---

## Environment Variables

```
# .env.example
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=ecommerce
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ecommerce
```

---

## Dataset

**Brazilian E-Commerce Public Dataset by Olist**
Licensed under [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
Source: [Kaggle](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

---

## Author

Ivan Caro Terrazas · [LinkedIn](https://linkedin.com/in/) · [GitHub](https://github.com/)
