with src_airport as ( select * from {{ ref('src_airport') }})

select
    {{ dbt_utils.generate_surrogate_key(['iata_code'])}} as airport_id,
    max(airport_name) as airport_name,
    iata_code,
    max(icao_code) as icao_code,
    max(continent) as continent,
    max(country) as country,
    max(location) as location
from src_airport
where iata_code is not null
group by iata_code