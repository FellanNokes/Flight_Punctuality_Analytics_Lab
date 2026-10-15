

with arrivals AS (select * from {{ ref('src_arrivals') }}),
via AS (select * from {{ ref('src_arrivals_via') }})

select
    {{ dbt_utils.generate_surrogate_key(['airline_icao']) }} AS airline_id,
    {{ dbt_utils.generate_surrogate_key(['arrival_iata']) }} AS arrival_airport_id,
    {{ dbt_utils.generate_surrogate_key(['departure_iata']) }} AS departure_airport_id,
    {{ dbt_utils.generate_surrogate_key(['flight_date']) }} AS date_id,
    a.flight_id,
    case
        when v._dlt_parent_id is not null then true
        else false
    end AS has_via_destination,
    a.di_indicator,
    a.arrival_time__schedule_utc,
    a.arrival_time__estimated_utc,
    a.arrival_time__actual_utc,
    a.terminal
from arrivals a
left join via v on a._dlt_id = v._dlt_parent_id
