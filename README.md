

A data engineering project that implements and compares **ETL** (Extract, Transform, Load) and **ELT** (Extract, Load, Transform) pipelines to process and analyze flight delay data from multiple sources.

Built as part of the **Data Engineering (DS437)** course at Princess Nourah Bint Abdulrahman University, College of Computer & Information Science.

---

## 📌 Project Overview

This project integrates flight delay data from two sources — a **Kaggle historical dataset** and the **AviationStack API** — to simulate real-world data engineering scenarios. It demonstrates two different approaches to building a data pipeline:

- **ETL Pipeline:** Data is extracted, cleaned and transformed using Python (pandas), then loaded into a local **SQLite** database.
- **ELT Pipeline:** Raw data is loaded directly into a **Neon PostgreSQL** cloud data warehouse, and all cleaning/transformation is performed afterward using **SQL**.

Both pipelines produce a structured dataset used to build **Power BI dashboards** for flight delay analysis and decision-making.

---

## 🗂️ Data Sources

| Source | Description |
|---|---|
| **Kaggle Flight Delays Dataset** | Historical flight records (airline, origin/destination, delays, cancellations) |
| **AviationStack API** | Live/recent flight data in JSON format |

---

## ⚙️ Project Structure

```
├── ETL.py                      # Main ETL pipeline: extract, transform, load into SQLite
├── ELT.py                      # ELT pipeline: load raw data into Neon PostgreSQL
├── ELT.txt                     # SQL transformation script run inside Neon (final_flight_delays table)
├── data_clean.py               # Cleans the raw Kaggle dataset before the ETL process
├── api_data.py                 # Fetches sample flight data from the AviationStack API
├── Flight_Delays_raw.csv       # Raw Kaggle dataset (with intentional data quality issues)
├── flight_delays_cleaned.csv   # Cleaned dataset (output of data_clean.py)
├── api_flights.csv             # Sample data pulled from the AviationStack API
└── README.md
```

---

## 🔄 ETL Pipeline (Python + SQLite)

1. **Extract** — Read the cleaned CSV dataset and pull live data from the AviationStack API.
2. **Transform** — Standardize column names, convert delay fields to numeric values, handle missing values, and create analytical columns (`total_delay`, `delay_status`, `data_source`).
3. **Load** — Merge both cleaned datasets and load them into a local SQLite database (`flights.db`).

**Result:** 502 records, 15 standardized columns, ready for SQL querying and dashboarding.

---

## 🔄 ELT Pipeline (Python + Neon PostgreSQL)

1. **Extract & Load (raw)** — Load the raw, unprocessed Kaggle and API datasets directly into staging tables (`stage_kaggle_raw`, `stage_api_raw`) in Neon PostgreSQL.
2. **Transform (inside the warehouse)** — Use SQL (`COALESCE`, `CASE`, `UNION ALL`) to clean missing values, standardize text, calculate `total_delay`, classify `delay_status`, and merge both sources into a final table: `final_flight_delays`.
3. **Export** — Export the transformed table to CSV/Excel for Power BI reporting.

The ELT workflow was also automated using a Python script (`elt_automation.py`) scheduled via **Windows Task Scheduler**. *(This automation script is documented in the project report but is not included in this repository.)*

---

## 📊 Dashboards

Both pipelines feed into interactive **Power BI dashboards** showing:
- Total flights, average delay, delayed vs. on-time flights
- Average delay by airline and by airport
- Delay trends over time
- Records by data source (Kaggle vs. AviationStack)

---

## 🆚 ETL vs. ELT — Key Findings

| Aspect | ETL (Python + SQLite) | ELT (Neon PostgreSQL) |
|---|---|---|
| **Execution Time** | 0.1736 sec | 0.294 sec |
| **Scalability** | Lower — limited by local RAM/pandas | Higher — benefits from database-level optimization |
| **Transformation Logic** | Handled in Python (more code complexity) | Handled in SQL (easier to maintain) |
| **Best Suited For** | Small/medium datasets, local processing | Large-scale, real-world analytical workloads |

**Conclusion:** The ELT approach proved more scalable and maintainable, making it better suited for real-world, large-scale data engineering use cases — while ETL remains a solid choice for smaller, well-defined datasets.

---

## 🛠️ Tools & Technologies

- **Python** (pandas, requests, sqlite3, SQLAlchemy)
- **SQLite** — local database for the ETL pipeline
- **Neon (Serverless PostgreSQL)** — cloud data warehouse for the ELT pipeline
- **AviationStack API** — live flight data source
- **Power BI** — data visualization and dashboards
- **Windows Task Scheduler** — ELT pipeline automation

---

## ▶️ How to Run

### ETL Pipeline
```bash
pip install pandas requests
python ETL.py
```
This generates a local `flights.db` SQLite database with the final cleaned `flights` table.

### ELT Pipeline
```bash
pip install pandas sqlalchemy psycopg2-binary
python ELT.py
```
> ⚠️ You'll need your own AviationStack API key and Neon PostgreSQL connection string. Set them as environment variables or replace the placeholder values in the scripts before running — **never commit real credentials to GitHub**.

Then run the SQL script in `ELT.txt` inside the Neon SQL editor to generate the `final_flight_delays` table.

---

## 👥 Project Info

**Course:** Data Engineering – DS437
**Instructor:** Dr. Shakila
**Institution:** Princess Nourah Bint Abdulrahman University — College of Computer & Information Science

---

## 📚 References

- [Kaggle — Flight Delays and Cancellations Dataset](https://www.kaggle.com/datasets/usdot/flight-delays)
- [AviationStack API Documentation](https://aviationstack.com/documentation)
- [IBM — ETL vs. ELT: What's the Difference?](https://www.ibm.com/topics/etl-vs-elt)
- [Neon — Serverless PostgreSQL Documentation](https://neon.tech/docs)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Microsoft Power BI Documentation](https://learn.microsoft.com/en-us/power-bi/)


