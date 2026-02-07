# Week 3 Homework: Data Warehousing & BigQuery

This repository contains the solution for Module 3 of the Data Engineering Zoomcamp 2026.

## 📂 Project Structure

* `main.tf`: Terraform configuration to set up the GCS Bucket and BigQuery Dataset.
* `load_yellow_taxi_data.py`: Python script to download 2024 Yellow Taxi data and upload it to GCS.
* `big_query_homework.sql`: All SQL queries used for analysis.

## 🛠️ Setup Instructions

1.  **Infrastructure**: Ran `terraform apply` to create GCS bucket and BQ dataset.
2.  **Ingestion**: Ran `python load_yellow_taxi_data.py` to upload Jan-Jun 2024 parquet files to GCS.
3.  **Warehousing**: Created External and Materialized tables in BigQuery.

## 📝 Homework Solutions

### Preparation: Create Tables

```sql
-- Create External Table
CREATE OR REPLACE EXTERNAL TABLE `your_project.your_dataset.external_yellow_tripdata`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your_bucket_name/yellow_tripdata_2024-*.parquet']
);

-- Create Materialized Table
CREATE OR REPLACE TABLE `your_project.your_dataset.yellow_tripdata_non_partitioned` AS
SELECT * FROM `your_project.your_dataset.external_yellow_tripdata`;
```

### Question 1: Count of records for the 2024 Yellow Taxi Data
**Answer: 20,332,093**

```sql
SELECT COUNT(*) FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`;
```

### Question 2: Estimated amount of data (External vs Materialized)
**Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table**

Query used for estimation:
```sql
SELECT COUNT(DISTINCT PULocationID) FROM `your_project.your_dataset.external_yellow_tripdata`;
SELECT COUNT(DISTINCT PULocationID) FROM `your_project.your_dataset.yellow_tripdata_non_partitioned`;
```

### Question 3: Why are the estimated number of Bytes different?
**Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

### Question 4: How many records have a fare_amount of 0?
**Answer: 8,333**

```sql
SELECT COUNT(*) FROM `your_project.your_dataset.yellow_tripdata_non_partitioned` WHERE fare_amount = 0;
```

### Question 5: Best strategy for optimization
**Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID**

### Question 6: Estimated bytes for Partitioned vs Non-Partitioned
**Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

Query used:
```sql
SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_tripdata_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```

### Question 7: Where is the data stored in the External Table?
**Answer: GCP Bucket**

### Question 8: Always cluster your data?
**Answer: False**

### Question 9: Bytes read for SELECT count(*)
**Answer: 0 Bytes**
(Explanation: BigQuery reads the row count from the table metadata.)