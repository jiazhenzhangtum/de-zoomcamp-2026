# Data Engineering Zoomcamp - Week 1 Homework

 Question 1. Knowing docker tags

Command used to check pip version:
docker run --rm python:3.13 pip --version

Question 2. Understanding docker first run
Answer: db:5432

Question 3. Count records
```sql
SELECT COUNT(*) 
FROM green_taxi_2025
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

Question 4. Longest trip for each day
```sql
SELECT 
    DATE(lpep_pickup_datetime) as pickup_day,
    MAX(trip_distance) as max_distance
FROM green_taxi_2025
WHERE lpep_pickup_datetime >= '2025-11-01' 
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance < 100
GROUP BY pickup_day
ORDER BY max_distance DESC
LIMIT 1;
```
Question 5. Three biggest pickup zones
```sql
SELECT 
    z."Zone", 
    SUM(t.total_amount) as total
FROM green_taxi_2025 t
JOIN zones z ON t."PULocationID" = z."LocationID"
WHERE DATE(t.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z."Zone"
ORDER BY total DESC
LIMIT 1;
```

Question 6. Largest tip
```sql
SELECT 
    z_drop."Zone", 
    MAX(t.tip_amount) as max_tip
FROM green_taxi_2025 t
JOIN zones z_pick ON t."PULocationID" = z_pick."LocationID"
JOIN zones z_drop ON t."DOLocationID" = z_drop."LocationID"
WHERE z_pick."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01' 
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY z_drop."Zone"
ORDER BY max_tip DESC
LIMIT 1;
```