with src_airport as {{ ref('src_airport') }}

select
    airport_name,
    iata_code,
    icao_code,
    continent,
    country,
    location
from src_airport