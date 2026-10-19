with all_airports as (
    select flight_leg_identifier__departure_airport_iata as iata,
           flight_leg_identifier__departure_airport_icao as icao,
           departure_airport_english as name
    from {{ source('flights', 'arrivals') }}
    union
    select flight_leg_identifier__arrival_airport_iata,
           flight_leg_identifier__arrival_airport_icao,
           arrival_airport_english
    from {{ source('flights', 'departures') }}
)

select distinct iata, icao, name
from all_airports
where icao like 'ES%'
  and iata not in (select iata_code from {{ ref('dim_airport') }})
order by iata