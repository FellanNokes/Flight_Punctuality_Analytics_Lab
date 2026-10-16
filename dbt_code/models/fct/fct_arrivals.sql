

with arrivals AS (select * from {{ ref('src_arrivals') }}),
via AS (select * from {{ ref('src_arrivals_via') }})

select
    {{ dbt_utils.generate_surrogate_key(['airline_icao']) }} AS airline_id,
    {{ dbt_utils.generate_surrogate_key(['arrival_iata']) }} AS arrival_airport_id,
    {{ dbt_utils.generate_surrogate_key(['departure_iata']) }} AS departure_airport_id,
    {{ dbt_utils.generate_surrogate_key(['flight_date']) }} AS date_id,
    a.flight_id,
    CASE
        WHEN v._dlt_parent_id is not null then true
        ELSE false
    END AS has_via_destination,
    CASE
        WHEN a.di_indicator = 'S' then 'Schengen'
        WHEN a.di_indicator = 'D' then 'Domestic'
        WHEN a.di_indicator = 'I' then 'International'
        ELSE 'Unknown'
    END AS type_of_flight,
    a.arrival_time_scheduled_utc,
    a.arrival_time_estimated_utc,
    a.arrival_time_actual_utc,
    a.terminal
from arrivals a
left join via v on a._dlt_id = v._dlt_parent_id
