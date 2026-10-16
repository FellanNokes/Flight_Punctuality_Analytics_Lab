select
    flight_leg_identifier__departure_airport_iata as iata,
    departure_airport_english,
    count(*) as n_flights
from {{ source('flights', 'arrivals') }}
where flight_leg_identifier__departure_airport_iata is null
   or upper(flight_leg_identifier__departure_airport_iata) not in (select iata_code from {{ ref('dim_airport') }})
group by 1, 2
order by 3 desc