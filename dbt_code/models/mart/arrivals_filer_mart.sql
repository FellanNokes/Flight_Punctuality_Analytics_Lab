

with 
    fct_arrivals as (select * from {{ ref('fct_arrivals') }}),
    dim_airlines as (select * from {{ ref('dim_airline') }}),
    dim_airports as (select * from {{ ref('dim_airport') }}),
    dim_date as (select * from {{ ref('dim_date') }})


select
    ap.airport_name,
    
from fct_arrivals f
left join dim_airline al on f.airline_id = al.airline_id
left join dim_airport ap on f.airport_id = ap.airport_id
left join dim_date d on f.date_id = d.date_id