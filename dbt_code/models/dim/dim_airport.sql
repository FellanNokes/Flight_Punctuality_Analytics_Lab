with src_airport as ( select * from {{ ref('src_airport') }})

select
    {{ dbt_utils.generate_surrogate_key(['iata_code'])}} as airport_id,
    airport_name,
    iata_code,
    icao_code,
    continent,
    country,
    location
from src_airport
where iata_code is not null