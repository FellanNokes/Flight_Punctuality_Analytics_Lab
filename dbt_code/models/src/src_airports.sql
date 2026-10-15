with airports as({{ source('wikipedia', 'airports') }})

select
    airline,
    iata,
    icao,
    country_region as country,
    comments
from airports