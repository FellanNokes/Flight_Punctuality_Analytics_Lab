with src_airline as ( select * from {{ ref('src_airline') }})

select
    {{ dbt_utils.generate_surrogate_key(['icao_code'])}} as airline_id,
    max(airline_name) as airline_name,
    max(iata_code) iata_code,
    icao_code,
    max(country) as country
from src_airline
where icao_code is not null 
    and (comments is null or comments not ilike '%defunct%')
group by icao_code
