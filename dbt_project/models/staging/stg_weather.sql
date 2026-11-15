select
    city,
    cast("time" as timestamp)               as measured_at,
    cast(temperature_2m as double)          as temperature_c,
    cast(relative_humidity_2m as double)    as humidity_pct,
    cast(wind_speed_10m as double)          as wind_speed_kmh,
    cast(wind_direction_10m as double)      as wind_direction_deg,
    cast(ingested_at as timestamp)          as ingested_at,
    city || '_' || "time"                   as weather_id
from {{ source('raw', 'weather') }}
