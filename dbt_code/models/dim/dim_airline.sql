with src_airline as (select * from {{ ref('src_airline') }})

select
    {{ dbt_utils.generate_surrogate_key(['icao_code']) }} as airline_id,
    airline_name,
    iata_code,
    icao_code,
    country
from src_airline
where icao_code is not null
qualify row_number() over (
    partition by icao_code
    order by
        coalesce(comments, '') ilike '%defunct%',
        iata_code is null,
        airline_name
) = 1
