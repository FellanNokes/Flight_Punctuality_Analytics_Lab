

with arrivals AS (select * from {{ ref('src_arrivals') }}),
via AS (select * from {{ ref('src_arrivals_via') }})

select
    {{ dbt_utils.generate_surrogate_key(['a.airline_icao']) }} AS airline_id,
    {{ dbt_utils.generate_surrogate_key(['a.arrival_iata']) }} AS arrival_airport_id,
    {{ dbt_utils.generate_surrogate_key(['a.departure_iata']) }} AS departure_airport_id,
    {{ dbt_utils.generate_surrogate_key(['a.flight_date']) }} AS date_id,
    a.flight_id,
    CASE
        WHEN v._dlt_parent_id is not null then true
        ELSE false
    END AS has_via_destination,
    CASE
        WHEN a.di_indicator = 'S' then 'Schengen'
        WHEN a.di_indicator = 'D' then 'Domestic'
        WHEN a.di_indicator = 'I' then 'International'
        ELSE 'unknown'
    END AS type_of_flight,
    a.arrival_time_scheduled_utc,
    a.arrival_time_estimated_utc,
    a.arrival_time_actual_utc,
    a.terminal,
    CASE
        WHEN a.arrival_time_scheduled_utc < a.arrival_time_actual_utc then true
        ELSE false
    END AS 'arrival_delayed',
    CASE
        WHEN 0 < (a.arrival_time_scheduled_utc - a.arrival_time_actual_utc) <= 5 then 'less_five_min'
        WHEN 6 <= (a.arrival_time_scheduled_utc - a.arrival_time_actual_utc) < 20 then '6_to_19'
        WHEN 20 <= (a.arrival_time_scheduled_utc - a.arrival_time_actual_utc) < 60 then '20_to_59'
        WHEN 60 <= (a.arrival_time_scheduled_utc - a.arrival_time_actual_utc) < 180 then '60_to_180'
        WHEN 180 <= (a.arrival_time_scheduled_utc - a.arrival_time_actual_utc) then 'over_180'
        ELSE 'not_delayed'
    END AS 'arrival_delayed_time'
from arrivals a
left join via v on a._dlt_id = v._dlt_parent_id
where a.arrival_time_actual_utc is not null
