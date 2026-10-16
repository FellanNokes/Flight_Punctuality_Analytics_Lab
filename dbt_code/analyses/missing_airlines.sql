select
    airline_operator__icao,
    airline_operator__name,
    count(*) as n_flights
from {{ source('flights', 'arrivals') }}
where airline_operator__icao is null
   or upper(airline_operator__icao) not in (select icao_code from {{ ref('dim_airline') }})
group by 1, 2
order by 3 desc