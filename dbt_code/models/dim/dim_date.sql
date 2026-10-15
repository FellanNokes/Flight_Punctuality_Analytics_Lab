with date_spine as (
    {{ dbt_utils.date_spine(
        datepart="day",
        start_date="cast('2026-10-01' as date)",
        end_date="cast('2027-01-01' as date)"
    ) }}
)

select
    {{ dbt_utils.generate_surrogate_key(['date_day']) }} as date_id,
    cast(date_day as date) as date,
    year(date_day) as year,
    month(date_day) as month,
    day(date_day) as day,
    dayname(date_day) as day_of_week,
    dayofweekiso(date_day) in (6, 7) as is_weekend
from date_spine