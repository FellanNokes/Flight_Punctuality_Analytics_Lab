USE ROLE flights_dlt_role;

USE DATABASE flights;

SHOW SCHEMAS;

SHOW TABLES IN SCHEMA staging;

DESC TABLE staging.arrivals;
DESC TABLE staging.departures;

-- Quick look at arrivals
SELECT
    flight_date,
    airport,
    flight_id,
    airline_operator__name,
    departure_airport_english,
    arrival_time__scheduled_utc,
    arrival_time__actual_utc,
    location_and_status__flight_leg_status
FROM staging.arrivals
LIMIT 50;

-- Check that flight_key is unique (both numbers should be equal)
SELECT
    COUNT(*) AS n_rows,
    COUNT(DISTINCT flight_key) AS n_keys
FROM staging.arrivals;

-- Arrivals per airport and day
SELECT airport, flight_date, COUNT(*) AS n_flights
FROM staging.arrivals
GROUP BY airport, flight_date
ORDER BY airport, flight_date;

-- Example filter: all arrivals to Arlanda operated by SAS
SELECT *
FROM staging.arrivals
WHERE airport = 'ARN'
  AND airline_operator__name ILIKE '%SAS%';