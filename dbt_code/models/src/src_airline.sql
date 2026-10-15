with stg_airlines as (select * from {{ source('wikipedia', 'airlines') }})

select
    airline as airline_name,
    iata as iata_code,
    icao as icao_code,
    country_region as country,
    comments
from stg_airlines