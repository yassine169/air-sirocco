-- Question métier 1 : dépassements des seuils journaliers OMS (2021)
-- PM2.5 : 15 µg/m³, PM10 : 45 µg/m³
with daily as (
    select
        city,
        cast(measured_at as date)  as day,
        avg(pm2_5)                 as avg_pm2_5,
        avg(pm10)                  as avg_pm10,
        max(dust)                  as max_dust,
        avg(case when is_south_wind then 1 else 0 end) as share_south_wind,
        count(*)                   as hours_measured
    from {{ ref('fct_air_hourly') }}
    group by 1, 2
)
select
    *,
    avg_pm2_5 > 15 as exceeds_who_pm2_5,
    avg_pm10  > 45 as exceeds_who_pm10,
    city || '_' || day as daily_id
from daily
