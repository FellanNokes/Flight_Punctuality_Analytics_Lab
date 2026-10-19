with src_airport as (
    select airport_name, iata_code, icao_code, continent, country, location
    from {{ ref('src_airport') }}

    union all

    select airport_name, iata_code, icao_code, continent, country, location
    from {{ ref('src_missing_airport') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['iata_code']) }} as airport_id,
    airport_name,
    iata_code,
    icao_code,
    continent,
    country,
    location
from src_airport
where iata_code is not null
qualify row_number() over (
    partition by iata_code
    order by
        icao_code is null,
        country
) = 1