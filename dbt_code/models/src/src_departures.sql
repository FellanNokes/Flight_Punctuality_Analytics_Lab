WITH stg_departures AS (SELECT * FROM {{ source('flights', 'departures') }})

SELECT
    flight_id,
    di_indicator,
    departure_time__scheduled_utc AS departure_time_scheduled_utc,
    departure_time__estimated_utc AS departure_time_estimated_utc,
    departure_time__actual_utc AS departure_time_actual_utc,
    flight_leg_identifier__departure_airport_iata AS departure_airport_iata,
    flight_leg_identifier__arrival_airport_iata AS arrival_airport_iata,
    airline_operator__icao AS airline_icao,
    location_and_status__terminal AS terminal,
    _dlt_id,
    flight_date,
FROM stg_departures
