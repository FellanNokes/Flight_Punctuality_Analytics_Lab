with stg_airports as({{ source('wikipedia', 'airports') }})

select
    airport,
    iata_code,
    icao_code,
    country_region as country,
    continent,
    country,
    location
from stg_airports