

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
    DATEDIFF(minute, a.arrival_time_scheduled_utc, a.arrival_time_actual_utc) AS arrival_delay_minutes,
    CASE
        WHEN DATEDIFF(minute, a.arrival_time_scheduled_utc, a.arrival_time_actual_utc) > 0 then 'Delayed'
        ELSE 'On Time'
    END AS arrival_status,
    CASE
        WHEN arrival_delay_minutes > 0 and arrival_delay_minutes < 5 then 'less_5_min'
        WHEN arrival_delay_minutes >= 5 and arrival_delay_minutes < 20 then '5_to_19'
        WHEN arrival_delay_minutes >= 20 and arrival_delay_minutes < 60 then '20_to_59'
        WHEN arrival_delay_minutes >= 60 and arrival_delay_minutes < 180 then '60_to_180'
        WHEN arrival_delay_minutes >= 180 then 'over_180'
        ELSE 'On Time'
    END AS arrival_delayed_time
from arrivals a
left join via v on a._dlt_id = v._dlt_parent_id
where a.arrival_time_actual_utc is not null
