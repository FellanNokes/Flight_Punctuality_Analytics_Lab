with 
    fct_departures as (select * from {{ ref('fct_departures') }}),
    dim_airline as (select * from {{ ref('dim_airline') }}),
    dim_airport as (select * from {{ ref('dim_airport') }}),
    dim_date as (select * from {{ ref('dim_date') }})


select
    ap.airport_name,
    COUNT(*) as amount_of_flights,
    sum(CASE WHEN f.departure_status = 'Delayed' then 1 else 0 END) as amount_delayed_departures,
    sum(CASE WHEN f.departure_status = 'On Time' then 1 else 0 END) as amount_not_delayed_departure,
    al.airline_name,
    CASE
        WHEN EXTRACT(HOUR FROM f.departure_time_scheduled_utc) <= 6 THEN 'night'
        WHEN EXTRACT(HOUR FROM f.departure_time_scheduled_utc) <= 12 THEN 'morning'
        WHEN EXTRACT(HOUR FROM f.departure_time_scheduled_utc) <= 18 THEN 'afternoon'
        WHEN EXTRACT(HOUR FROM f.departure_time_scheduled_utc) < 24 THEN 'evening'
        ELSE 'unknown'
    END AS time_period,
    f.type_of_flight,
    ap.continent,
    ap.country,
    f.departure_delayed_time,
    d.day_of_week,
    d.date
from fct_departures f
left join dim_airline al on f.airline_id = al.airline_id
left join dim_airport ap on f.arrival_airport_id = ap.airport_id
left join dim_date d on f.date_id = d.date_id
group by
    ap.airport_name,
    al.airline_name,
    time_period,
    f.type_of_flight,
    ap.continent,
    ap.country,
    f.departure_delayed_time,
    d.day_of_week,
    d.date