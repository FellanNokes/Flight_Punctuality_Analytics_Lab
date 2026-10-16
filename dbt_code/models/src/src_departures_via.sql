WITH stg_via_des AS (SELECT * FROM {{ source('flights', 'departures_via_destinations') }})

SELECT
    _dlt_parent_id,
    airport_iata,
    airport_english
FROM stg_via_des