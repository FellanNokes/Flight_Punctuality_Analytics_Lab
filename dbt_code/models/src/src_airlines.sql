with stg_airlines as {{ source('wikipedia', 'airlines') }}

select
    airline,
    iata,
    icao,
    country_region as country,
    comments
from stg_airlines