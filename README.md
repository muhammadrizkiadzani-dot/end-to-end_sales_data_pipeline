# End-to-End Sales Data Pipeline: Cleaning and Processing Dirty Data Using Python (Pandas) and PostgreSQL

## Project Overview
In real-world industries, raw transactional data is rarely clean. This project demonstrates an end-to-end data engineering and analytics pipeline designed to extract, transform, and ingest a chaotic, multi-city retail transactional dataset into a production-ready PostgreSQL database. 

By building this pipeline, I successfully established rigorous **data quality** controls, handled multiple data anomalies, and performed feature engineering to make the dataset fully optimized for database warehousing, business intelligence dashboards, and deep operational trend analysis.

---

## Tech Stack & Tools
- **Language:** Python , SQL
- **Libraries:** Pandas (Data Manipulation), SQLAlchemy & Psycopg2 (Database Ingestion)
- **Database Warehouse:** PostgreSQL
- **Dataset:** 500 rows of raw, unstandardized transactional data spanning multiple cities (Jakarta, Bandung, Surabaya, Medan, Yogyakarta).

---

## Key Pipeline Features & Transformation Steps

### 1. Data Cleaning & Standardization
- **Currency & Numeric Refinement:** Stripped currency symbols ("Rp"), removed thousands separators (dots), and converted the `Harga_Satuan` column into standard integers for mathematical operations.
- **Text Uniformity:** Handled string variations by stripping hidden whitespaces, converting `Produk` names to strict UPPERCASE, and standardizing `Kota_Toko` names to Title Case to eliminate categorical duplication.
- **Inconsistent Date Parsing:** Resolved chaotic, mixed-format date entries (e.g., "08/08/2025", "Aug 4, 2025", "2025-09-13") using modern datetime parsing to enforce structural data integrity.

### 2. Anomaly Detection & Quality Control
- **Negative Values Isolation:** Built a validation layer to identify and isolate faulty system logs, such as negative order quantities (`Jumlah < 0`), preventing them from skewing business logic.
- **Deduplication:** Identified and eliminated duplicate transaction rows to preserve data accuracy.
- **Structural Missing Value Handling:** Strategically removed incomplete rows missing critical primary keys (`ID_Transaksi` and `Harga_Satuan`), while safely filling other missing parameters with strict fallback defaults (`TRX-UNKNOWN`, `PRODUK-UNKNOWN`).

### 3. Feature Engineering
- **Time Intelligence:** Extracted month numbers and mapped them to local Indonesian month names (`Januari` - `Desember`) to facilitate chronological sales tracking.
- **Business Performance Tracking:** Created a calculated column `Total_Penjualan` (`Jumlah` * `Harga_Satuan`) to serve as a core revenue metric for operations teams.

### 4. Database Ingestion (Load)
- Automated the transmission of the finalized, clean dataset into a localized **PostgreSQL database warehouse** (`produksi_db`) using `SQLAlchemy` with a direct data-overwrite replacement strategy.

---

## Production-Ready Business Queries (`business_queries.sql`)
Once the clean data is safely ingested into PostgreSQL, I developed an analytical layer consisting of optimized SQL business queries designed to unlock actionable insights for management:

1. **Trend Analysis (Monthly Revenue Performance):** Aggregates total monthly revenue and average transaction values to help operations monitor seasonal demand cycles.
2. **Operational Efficiency (Top Invoicing Tracking):** Isolates the highest-value transactions and total item quantities per invoice to assist logistics team handling.
3. **Geographical Breakdown (Branch Performance):** Ranks branch cities by total unique transactions and revenue generation to optimize regional supply chain distribution.
4. **Inventory Management (Top Products Analytics):** Identifies the top 5 high-demand items to prevent stockout scenarios and support demand forecasting.
5. **Quality Control & Audit (Operational Anomaly Scanning):** Runs automated data integrity audits to instantly catch any broken records or systemic logging failures.

---

## How to Run the Project

1. **Prerequisites:** Ensure you have PostgreSQL running locally and python packages installed:
   ```bash
   pip install pandas sqlalchemy psycopg2
   ```
2. **Database Setup:** Create a local database named `produksi_db`.
3. **Execution:** Update the database credentials in the script and run it:
   ```bash
   data_pipeline.py
   ```
4. **Analytics:** Open your PostgreSQL tool (e.g., pgAdmin) and execute the scripts inside `business_queries.sql` to generate executive reports.

---

## Business Insights Generated
By establishing this automated pipeline and query layer, the data is now structured to easily unlock:
- Monthly operational and sales volume trends.
- Revenue breakdown and performance analysis per city branch.
- Inventory movement tracking to support demand forecasting.
