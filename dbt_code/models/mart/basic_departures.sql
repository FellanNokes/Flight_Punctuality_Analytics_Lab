with 
    fct_departures as (select * from {{ ref('fct_departures') }}),
    dim_airline as (select * from {{ ref('dim_airline') }}),
    dim_airport as (select * from {{ ref('dim_airport') }}),
    dim_date as (select * from {{ ref('dim_date') }})


select
    ap.airport_name,
    COUNT(*) as amount_of_flights,
    sum(CASE WHEN de.departure_status = 'Delayed' then 1 else 0 END) as amount_delayed_flights_departures,
    sum(CASE WHEN de.departure_status = 'On Time' then 1 else 0 END) as amount_not_delayed_departure,
    al.airline_name,
    de.departure_delayed_time,
    d.date
from fct_departures de
left join dim_airline al on de.airline_id = al.airline_id
left join dim_airport ap on de.departure_airport_id = ap.airport_id
left join dim_date d on de.date_id = d.date_id
group by
    ap.airport_name,
    al.airline_name,
    de.departure_delayed_time,
    d.date