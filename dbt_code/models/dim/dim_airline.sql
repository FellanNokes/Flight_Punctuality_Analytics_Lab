with src_airline as {{ ref('src_airline') }}

select
    airline_name,
    iata_code,
    icao_code,
    country_region
from src_airline