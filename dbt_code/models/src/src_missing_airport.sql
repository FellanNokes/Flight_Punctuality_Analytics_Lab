with missing_airports as (select * from {{ ref('missing_airports') }})

select
    airport_name,
    iata_code,
    icao_code,
    continent,
    country,
    location
from missing_airports