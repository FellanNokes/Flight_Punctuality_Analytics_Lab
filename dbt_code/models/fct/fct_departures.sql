with departures AS (select * from {{ ref('src_departures') }}),
via_dest AS (select * from {{ ref('src_departures_via') }})

SELECT
    {{ dbt_utils.generate_surrogate_key(['d.airline_icao']) }} as airline_id,
    {{ dbt_utils.generate_surrogate_key(['d.arrival_airport_iata']) }} as arrival_airport_id,
    {{ dbt_utils.generate_surrogate_key(['d.departure_airport_iata']) }} as departure_airport_id,
    {{ dbt_utils.generate_surrogate_key(['d.departure_time_actual_utc']) }} as date_id,
    d.flight_id,
    CASE
        WHEN v._dlt_parent_id is not null then true
        ELSE false
    END AS has_via_destination,
    d.di_indicator,
    CASE
        WHEN d.di_indicator = 'S' then 'Schengen'
        WHEN d.di_indicator = 'D' then 'Domestic'
        WHEN d.di_indicator = 'I' then 'International'
        ELSE 'Unknown'
    END AS Type_of_flight,
    d.departure_time_scheduled_utc,
    d.departure_time_estimated_utc,
    d.departure_time_actual_utc,
    d.terminal
FROM departures d
LEFT JOIN via_dest v ON d._dlt_id = v._dlt_parent_id