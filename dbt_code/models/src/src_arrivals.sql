

with arrivals AS (select * from {{ source('flights', 'arrivals') }})

select
    flight_id,
    di_indicator,
    arrival_time__scheduled_utc AS arrival_time_scheduled_utc,
    arrival_time__estimated_utc AS arrival_time_estimated_utc,
    arrival_time__actual_utc AS arrival_time_actual_utc,
    location_and_status__terminal AS terminal,
    airline_operator__icao AS airline_icao,
    flight_leg_identifier__arrival_airport_iata AS arrival_iata,
    flight_leg_identifier__departure_airport_iata AS departure_iata,
    _dlt_id,
    flight_date
from arrivals