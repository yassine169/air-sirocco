-- Une ligne par ville et par heure : pollution + météo
select
    a.city,
    a.measured_at,
    a.pm2_5,
    a.pm10,
    a.dust,
    a.no2,
    a.ozone,
    w.temperature_c,
    w.humidity_pct,
    w.wind_speed_kmh,
    w.wind_direction_deg,
    -- Vent venant du sud (secteur 135°-225°) : signature du sirocco
    coalesce(w.wind_direction_deg between 135 and 225, false) as is_south_wind
from {{ ref('stg_air_quality') }} a
left join {{ ref('stg_weather') }} w
    on a.city = w.city and a.measured_at = w.measured_at
