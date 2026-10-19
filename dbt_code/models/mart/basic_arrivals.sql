with 
    fct_arrivals as (select * from {{ ref('fct_arrivals') }}),
    dim_airline as (select * from {{ ref('dim_airline') }}),
    dim_airport as (select * from {{ ref('dim_airport') }}),
    dim_date as (select * from {{ ref('dim_date') }})


select
    ap.airport_name,
    COUNT(*) as amount_of_flights,
    sum(CASE WHEN f.arrival_status = 'Delayed' then 1 else 0 END) as amount_delayed_flights_arrivals,
    sum(CASE WHEN f.arrival_status = 'On Time' then 1 else 0 END) as amount_not_delayed_arrival,
    al.airline_name,
    f.arrival_delayed_time,
    d.date
from fct_arrivals f
left join dim_airline al on f.airline_id = al.airline_id
left join dim_airport ap on f.arrival_airport_id = ap.airport_id
left join dim_date d on f.date_id = d.date_id
group by
    ap.airport_name,
    al.airline_name,
    f.arrival_delayed_time,
    d.date