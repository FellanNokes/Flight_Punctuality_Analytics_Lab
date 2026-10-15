with stg_airports as(select * from {{ source('wikipedia', 'airports') }})

select
    airport as airport_name,
    iata_code,
    icao_code,
    continent,
    country,
    location
from stg_airports