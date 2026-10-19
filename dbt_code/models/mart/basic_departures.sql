WITH fct_dep AS (SELECT * FROM {{ ref('fct_departures') }})
dim_date AS (SELECT * FROM {{ ref('dim_date') }}),
dim_port AS (SELECT * FROM {{ ref('dim_airport') }}),
dim_line AS (SELECT * FROM {{ ref('dim_airline') }}),

SELECT
    f.airline_id,
    f.arrival_airport_id,
    f.departure_airport_id,
    f.date_id,
    d.date,
    d.year,
    d.month,
    d.day,
    d.day_of_week,
    d.is_weekend,
    flight_id,
    has_via_destination,
    type_of_flight,
    departure_time_scheduled_utc,
    departure_time_estimated_utc,
    departure_time_actual_utc,
    terminal

FROM fct_dep f
LEFT JOIN dim_date d ON f.date_id = d.date_id
LEFT JOIN dim_port p ON f.departure_airport_id = p.airport_id
LEFT JOIN dim_port p ON f.arrival_airport_id = p.airport_id
LEFT JOIN dim_line l ON f.airline_id = l.airline_id
