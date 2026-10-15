with via_destinations AS (select * from {{ source('flights', 'arrivals_via_destinations') }})

select
    _dlt_parent_id,
    airport_iata,
    airport_english
from via_destinations